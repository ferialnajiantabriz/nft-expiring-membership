// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title NFTMembership
 * @dev A time-based NFT membership with expiration logic.
 */
contract NFTMembership is ERC721, Ownable {
    // Next tokenId tracker
    uint256 private _currentTokenId;

    // Mapping tokenId -> expiration timestamp
    mapping(uint256 => uint256) public validUntil;

    // Price to mint or renew membership (you can adapt this)
    uint256 public membershipPrice;

    // Event to log membership renewals
    event MembershipRenewed(uint256 indexed tokenId, uint256 newExpiry);

    constructor(
        string memory name_,
        string memory symbol_,
        uint256 initialPrice
    ) ERC721(name_, symbol_) {
        membershipPrice = initialPrice; 
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
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        require(msg.value >= membershipPrice, "Insufficient payment");
        require(isValid(tokenId), "Membership expired, cannot renew");

        validUntil[tokenId] += additionalTime;
        emit MembershipRenewed(tokenId, validUntil[tokenId]);
    }

    /**
     * @dev Set a new membership price (only the contract owner can call).
     */
    function setMembershipPrice(uint256 newPrice) external onlyOwner {
        membershipPrice = newPrice;
    }
}

