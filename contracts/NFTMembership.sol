// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title NFTMembership
 * @dev An ERC721-based membership token with an expiration date. It uses AccessControl
 * for admin management and supports meta-transactions via a trusted forwarder (EIP-2771).
 */
contract NFTMembership is ERC721, AccessControl {
    // Custom role for managing pricing and admin tasks
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // Tracks membership expiration timestamps
    mapping(uint256 => uint256) public validUntil;

    // Price to mint or renew (in Wei)
    uint256 public membershipPrice;

    // Token ID counter
    uint256 private _tokenIdCounter;

    // Meta-transaction trusted forwarder
    address public trustedForwarder;

    // Event for successful renewals
    event MembershipRenewed(uint256 indexed tokenId, uint256 newExpiry);

    /**
     * @dev Constructor: sets up initial roles and parameters.
     * @param name_ Token name (e.g., "MembershipPass")
     * @param symbol_ Token symbol (e.g., "MBR")
     * @param initialPrice Initial membership price in Wei
     * @param forwarder Address of EIP-2771 forwarder
     */
    constructor(
        string memory name_,
        string memory symbol_,
        uint256 initialPrice,
        address forwarder
    ) ERC721(name_, symbol_) {
        // Grant full control to deployer
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(ADMIN_ROLE, msg.sender);

        membershipPrice = initialPrice;
        trustedForwarder = forwarder;
    }

    /**
     * @dev OpenZeppelin required override for AccessControl + ERC721
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC721, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    /**
     * @dev EIP-2771: checks if caller is a trusted forwarder
     */
    function isTrustedForwarder(address forwarder) public view virtual returns (bool) {
        return forwarder == trustedForwarder;
    }

    /**
     * @dev Admin-only: sets a new price for mint/renew
     * @param newPrice New membership price in Wei
     */
    function setMembershipPrice(uint256 newPrice) external onlyRole(ADMIN_ROLE) {
        membershipPrice = newPrice;
    }

    /**
     * @dev Admin-only: grant ADMIN_ROLE to an address
     */
    function grantAdminRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(ADMIN_ROLE, account);
    }

    /**
     * @dev Admin-only: revoke ADMIN_ROLE from an address
     */
    function revokeAdminRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(ADMIN_ROLE, account);
    }

    /**
     * @dev Mints a new membership NFT for `recipient`.
     * @param recipient Address receiving the NFT
     * @param durationInSeconds Time before expiry (in seconds)
     */
    function mintMembership(address recipient, uint256 durationInSeconds) external payable {
        require(msg.value >= membershipPrice, "Insufficient payment");

        _tokenIdCounter++;
        uint256 newTokenId = _tokenIdCounter;

        _safeMint(recipient, newTokenId);
        validUntil[newTokenId] = block.timestamp + durationInSeconds;
    }

    /**
     * @dev Renews an existing membership token.
     * @param tokenId Token to renew
     * @param additionalSeconds Time to extend
     */
    function renewMembership(uint256 tokenId, uint256 additionalSeconds) external payable {
        require(msg.value >= membershipPrice, "Insufficient payment");
        require(ownerOf(tokenId) == msg.sender, "Not token owner");

        uint256 currentExpiry = validUntil[tokenId];
        if (block.timestamp > currentExpiry) {
            currentExpiry = block.timestamp;
        }

        uint256 newExpiry = currentExpiry + additionalSeconds;
        validUntil[tokenId] = newExpiry;

        emit MembershipRenewed(tokenId, newExpiry);
    }

    /**
     * @dev Allows relayer to submit a gasless renewal using EIP-2771
     */
    function metaRenewMembership(
        uint256 tokenId,
        uint256 additionalSeconds,
        address realUser
    ) external {
        require(isTrustedForwarder(msg.sender), "Not trusted forwarder");
        require(ownerOf(tokenId) == realUser, "Not token owner");

        uint256 currentExpiry = validUntil[tokenId];
        if (block.timestamp > currentExpiry) {
            currentExpiry = block.timestamp;
        }

        uint256 newExpiry = currentExpiry + additionalSeconds;
        validUntil[tokenId] = newExpiry;

        emit MembershipRenewed(tokenId, newExpiry);
    }

    /**
     * @dev EIP-2771: Override msg.sender if forwarded
     */
    function _msgSender() internal view override returns (address sender) {
        if (isTrustedForwarder(msg.sender)) {
            assembly {
                sender := shr(96, calldataload(sub(calldatasize(), 20)))
            }
        } else {
            sender = super._msgSender();
        }
    }

    /**
     * @dev EIP-2771: Override msg.data if forwarded
     */
    function _msgData() internal view override returns (bytes calldata) {
        if (isTrustedForwarder(msg.sender)) {
            return msg.data[:msg.data.length - 20];
        } else {
            return super._msgData();
        }
    }
}
