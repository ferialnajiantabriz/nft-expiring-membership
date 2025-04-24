// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title NFTMembership
 * @dev An ERC721-based membership token with an expiration date. It uses AccessControl
 * for admin management and supports meta-transactions by trusting a forwarder address.
 */
contract NFTMembership is ERC721, AccessControl {
    // Use a custom role identifier
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // Maps each tokenId to its expiration timestamp
    mapping(uint256 => uint256) public validUntil;

    // The price for minting or renewing a membership (in Wei)
    uint256 public membershipPrice;

    // Tracks the next token ID to mint
    uint256 private _tokenIdCounter;

    // Emitted when a membership is renewed
    event MembershipRenewed(uint256 indexed tokenId, uint256 newExpiry);

    // The forwarder permitted to call metaRenewMembership (if you use EIP-2771 meta-transactions)
    address public trustedForwarder;

    /**
     * @dev Constructor sets up initial roles, price, and forwarder.
     * @param name_ The ERC721 name, e.g., "MembershipPass"
     * @param symbol_ The ERC721 symbol, e.g., "MBR"
     * @param initialPrice The initial membership price in Wei
     * @param forwarder The address of the trusted forwarder for meta-transactions
     */
    constructor(
        string memory name_,
        string memory symbol_,
        uint256 initialPrice,
        address forwarder
    ) ERC721(name_, symbol_) {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(ADMIN_ROLE, msg.sender);

        membershipPrice = initialPrice;
        trustedForwarder = forwarder;
    }

    /**
     * @dev Required override since both ERC721 and AccessControl define supportsInterface().
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
     * @dev Check if a given forwarder is our trusted forwarder. Used in EIP-2771 flow.
     * @param forwarder The address we want to verify
     */
    function isTrustedForwarder(address forwarder) public view virtual returns (bool) {
        return forwarder == trustedForwarder;
    }

    /**
     * @dev Allows an admin to update the membership price.
     * @param newPrice The new price in Wei
     */
    function setMembershipPrice(uint256 newPrice) external onlyRole(ADMIN_ROLE) {
        membershipPrice = newPrice;
    }

    /**
     * @dev Mints a new membership NFT with an expiration of (now + durationInSeconds).
     * Requires `msg.value` >= membershipPrice.
     * @param recipient The address to receive the new NFT
     * @param durationInSeconds How long (in seconds) before the membership expires
     */
    function mintMembership(address recipient, uint256 durationInSeconds) external payable {
        require(msg.value >= membershipPrice, "Insufficient payment");

        _tokenIdCounter++;
        uint256 newTokenId = _tokenIdCounter;

        _safeMint(recipient, newTokenId);
        validUntil[newTokenId] = block.timestamp + durationInSeconds;
    }

    /**
     * @dev Renews a membership by extending its validUntil.
     * Requires `msg.value` >= membershipPrice.
     * @param tokenId The token to renew
     * @param additionalSeconds How many extra seconds to add
     */
    function renewMembership(uint256 tokenId, uint256 additionalSeconds) external payable {
        require(msg.value >= membershipPrice, "Insufficient payment");
        require(ownerOf(tokenId) == msg.sender, "Not token owner");

        uint256 currentExpiry = validUntil[tokenId];
        // If the membership is already expired, restart from now
        if (block.timestamp > currentExpiry) {
            currentExpiry = block.timestamp;
        }

        uint256 newExpiry = currentExpiry + additionalSeconds;
        validUntil[tokenId] = newExpiry;

        emit MembershipRenewed(tokenId, newExpiry);
    }

    /**
     * @dev Called by the trusted forwarder only. Allows gasless renewal for the `realUser`.
     * Off-chain, the user signs a message, and the forwarder pays the gas to call this function.
     * @param tokenId The token to renew
     * @param additionalSeconds Extra time in seconds to add
     * @param realUser The real user who owns the token
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
     * @dev EIP-2771 override: returns the real sender of this call if it came through a trusted forwarder.
     */
    function _msgSender() internal view override returns (address sender) {
        if (isTrustedForwarder(msg.sender)) {
            // The last 20 bytes of msg.data is the address of the real sender appended by forwarder
            assembly {
                sender := shr(96, calldataload(sub(calldatasize(), 20)))
            }
        } else {
            sender = super._msgSender();
        }
    }

    /**
     * @dev EIP-2771 override: returns the real msg.data if it came through a trusted forwarder.
     */
    function _msgData() internal view override returns (bytes calldata) {
        if (isTrustedForwarder(msg.sender)) {
            return msg.data[:msg.data.length - 20];
        } else {
            return super._msgData();
        }
    }
}
