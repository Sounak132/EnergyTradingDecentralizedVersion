import functions as F
import entities as e
from ecdsa import SECP256k1

curve_type = SECP256k1
(sk_hex, vk_hex) = F.generate_keys(curve_type)

sk1 = F.get_private_key(sk_hex, curve_type)
vk1 = F.get_public_key(vk_hex, curve_type)

print("Private key: {} \nPublic key: {}".format(sk1.to_string(), vk1.to_string()))