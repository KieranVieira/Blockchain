import hashlib
import requests
import json

import sys

# TODO: Implement functionality to search for a proof 
def get_last_block():
    response = requests.get("http://localhost:5000/last-block")

    return json.loads(response.content)

def look_for_proof():
    last_block = get_last_block()

    block_string = json.dumps(last_block, sort_keys=True)
    proof = 0

    def is_proof_valid():
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == '000000'

    while is_proof_valid() is False:
        print(proof)
        proof += 1

    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        new_proof = look_for_proof()
        # TODO: When found, POST it to the server {"proof": new_proof}
        response = requests.post("http://localhost:5000/mine", json={"proof": new_proof})
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        content = json.loads(response.content)
        print(content)
        if content["message"] == "New Block Forged":
            coins_mined += 1
            print(f"Proof of {new_proof} found! You got 1 coin for destroying your GPU.")
            print(f"you now have mined {coins_mined} coin(s).")
        else:
            print(content["message"])
