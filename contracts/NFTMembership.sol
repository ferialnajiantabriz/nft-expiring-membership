// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title NFTMembership
 * @dev A time-based NFT membership with expiration logic.
 */
contract NFTMembership is ERC721, Ownable, AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // Next tokenId tracker
    uint256 private _currentTokenId;

    // Mapping tokenId -> expiration timestamp
    mapping(uint256 => uint256) public validUntil;

    // Price to mint or renew membership
    uint256 public membershipPrice;

    // Event to log membership renewals
    event MembershipRenewed(uint256 indexed tokenId, uint256 newExpiry);

    constructor(
        string memory name_,
        string memory symbol_,
        uint256 initialPrice
    ) ERC721(name_, symbol_) {
        membershipPrice = initialPrice;
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    /**
     * @dev Mint a new membership NFT with an expiration time.
     * @param recipient The address that will own the NFT
     * @param duration  The duration (in seconds) for which the membership is valid
     */
    function mintMembership(address recipient, uint256 duration)
        external
        payable
    {
        require(msg.value >= membershipPrice, "Insufficient payment");
        _currentTokenId++;
        uint256 newTokenId = _currentTokenId;

        // Mint the NFT
        _safeMint(recipient, newTokenId);

        // Set expiration
        validUntil[newTokenId] = block.timestamp + duration;
    }

    /**
     * @dev Check if a token is still valid (not expired).
     */
    function isValid(uint256 tokenId) public view returns (bool) {
        return (block.timestamp <= validUntil[tokenId]);
    }

    /**
     * @dev Renew membership for a specific token.
     * @param tokenId The token ID to renew
     * @param additionalTime The extra time (in seconds) to add
     */
    function renewMembership(uint256 tokenId, uint256 additionalTime)
        external
        payable
    {
        // Only the token owner can renew
        require(ownerOf(tokenId) == msg.sender, "Not token owner");

        // Payment check
        require(msg.value >= membershipPrice, "Insufficient payment");

        // Must not be expired
        require(isValid(tokenId), "Membership expired, cannot renew");

        // Extend expiration
        validUntil[tokenId] += additionalTime;

        emit MembershipRenewed(tokenId, validUntil[tokenId]);
    }

    /**
     * @dev Set a new membership price. Only an address with ADMIN_ROLE can call this.
     */
    function setMembershipPrice(uint256 newPrice) external {
        require(hasRole(ADMIN_ROLE, msg.sender), "Caller is not an admin");
        membershipPrice = newPrice;
    }

    /**
     * @dev Overriding supportsInterface to handle multiple inheritance from ERC721 & AccessControl.
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
