// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @dev MinimalForwarder to support meta-transactions (gasless transactions).
 * Follows EIP-2771 standard approach.
 */
contract MinimalForwarder {
    struct ForwardRequest {
        address from;
        address to;
        uint256 value;
        uint256 gas;
        uint256 nonce;
        bytes data;
    }

    mapping(address => uint256) private _nonces;

    function getNonce(address from) public view returns (uint256) {
        return _nonces[from];
    }

    /**
     * @dev Verifies the signature for a given ForwardRequest.
     */
    function verify(
        ForwardRequest calldata req,
        bytes calldata signature
    ) public view returns (bool) {
        bytes32 hash = _hashTypedData(req);
        address signer = _recover(hash, signature);
        return (signer == req.from && _nonces[req.from] == req.nonce);
    }

    /**
     * @dev Executes the meta-tx if signature is valid.
     * Increments the nonce, then calls the requested function.
     */
    function execute(
        ForwardRequest calldata req,
        bytes calldata signature
    ) public payable returns (bool, bytes memory) {
        require(verify(req, signature), "MinimalForwarder: signature does not match request");
        _nonces[req.from]++;

        (bool success, bytes memory returndata) = req.to.call{gas: req.gas, value: req.value}(
            abi.encodePacked(req.data, req.from)
        );
        // Validate that the relayer has sent enough gas
        // and the call didn't run out of gas.
        require(gasleft() > req.gas / 63, "MinimalForwarder: out of gas");

        return (success, returndata);
    }

    /**
     * @dev Creates EIP712 typed data hash.
     */
    function _hashTypedData(ForwardRequest calldata req) private pure returns (bytes32) {
        // EIP712 domain separator can be simplified for a minimal forwarder
        return keccak256(
            abi.encodePacked(
                "\x19\x01",
                // Hash of the domain separator, minimal version
                keccak256(abi.encode(
                    keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
                    keccak256(bytes("MinimalForwarder")),
                    keccak256(bytes("1")),
                    0, // chainId not strictly validated here
                    address(0) // verifyingContract not strictly validated
                )),
                keccak256(abi.encode(
                    keccak256("ForwardRequest(address from,address to,uint256 value,uint256 gas,uint256 nonce,bytes data)"),
                    req.from,
                    req.to,
                    req.value,
                    req.gas,
                    req.nonce,
                    keccak256(req.data)
                ))
            )
        );
    }

    /**
     * @dev Recovers signer address from signature.
     */
    function _recover(bytes32 hash, bytes calldata signature) private pure returns (address) {
        // Standard ECDSA signature check
        if (signature.length != 65) {
            return address(0);
        }

        bytes32 r;
        bytes32 s;
        uint8 v;
        
        // Signature layout is r(32 bytes), s(32 bytes), v(1 byte)
        assembly {
            r := calldataload(signature.offset)
            s := calldataload(add(signature.offset, 32))
            v := byte(0, calldataload(add(signature.offset, 64)))
        }

        return ecrecover(hash, v, r, s);
    }
}

