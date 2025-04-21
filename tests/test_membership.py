import pytest
from brownie import NFTMembership, accounts, reverts

@pytest.fixture
def membership_contract():
    # Deploy the contract using the first account
    yield NFTMembership.deploy(
        "MembershipPass",
        "MBR",
        10**16,  # example price: 0.01 ETH
        {'from': accounts[0]}
    )

def test_mint_membership(membership_contract, accounts):
    # Mint with 0.01 ETH
    membership_contract.mintMembership(
        accounts[1],
        3600,  # 1 hour in seconds
        {'from': accounts[1], 'value': 10**16}
    )
    assert membership_contract.ownerOf(1) == accounts[1]
    assert membership_contract.isValid(1) == True

def test_insufficient_payment(membership_contract, accounts):
    with reverts("Insufficient payment"):
        membership_contract.mintMembership(
            accounts[1],
            3600,
            {'from': accounts[1], 'value': 0}
        )

def test_renew_membership(membership_contract, accounts, chain):
    # Mint token first
    membership_contract.mintMembership(
        accounts[1],
        3600,
        {'from': accounts[1], 'value': 10**16}
    )
    token_id = 1

    # Move time forward ~3000 seconds
    chain.sleep(3000)
    chain.mine()

    # Renew with another hour
    membership_contract.renewMembership(
        token_id,
        3600,
        {'from': accounts[1], 'value': 10**16}
    )
    assert membership_contract.isValid(token_id) == True

def test_expired_membership(membership_contract, accounts, chain):
    membership_contract.mintMembership(
        accounts[1],
        1,
        {'from': accounts[1], 'value': 10**16}
    )
    token_id = 1

    # Sleep 5 seconds -> membership should expire
    chain.sleep(5)
    chain.mine()

    assert membership_contract.isValid(token_id) == False

    with reverts("Membership expired, cannot renew"):
        membership_contract.renewMembership(
            token_id,
            3600,
            {'from': accounts[1], 'value': 10**16}
        )

