MINECART = {
    "set": "[~] {p} sets a TNT minecart on a powered rail...",
    "disarm": "[=] {p2} break{s} {p}'s TNT minecart.",
    "escape": "[=] {p2} trigger{s} {p}'s TNT minecart, but survive{s} the explosion.",
    "kill": "[-] {p2} {w} blown up by {p}'s TNT minecart trap",
}

FALL = {
    "set": "[~] {p} digs a deep pit in the ground...",
    "disarm": "[=] {p2} cover{s} the hole left by {p}.",
    "escape": "[=] {p2} fall{s} into {p}'s trap, but survive{s}.",
    "kill": "[-] {p2} fell from a high place, thanks to {p}'s trap",
}

LAVA = {
    "set": "[~] {p} puts down a few buckets of lava...",
    "disarm": "[=] {p2} block{s} up {p}'s lava.",
    "escape": "[=] {p2} fall{s} into {p}'s lava, but escape{s} and puts themselves out.",
    "kill": "[-] {p2} tried to swim in {p}'s lava trap"
}

SKULK = {
    "set": "[~] {p} links a skulk sensor to a pile of TNT...",
    "disarm": "[=] {p2} break{s} {p}'s sensor.",
    "escape": "[=] {p2} trigger{s} {p}'s sensor, but survive{s} the explosion.",
    "kill": "[-] {p2} {w} blown up by {p}'s skulk sensor trap"
}

OBSERVER = {
    "set": "[~] {p} links an observer to a powered rail...",
    "disarm": "[=] {p2} dig{s} around until they find and break {p}'s observer.",
    "escape": "[=] {p2} trigger{s} {p}'s observer, but survive{s} the explosion.",
    "kill": "[-] {p2} {w} blown up by {p}'s observer trap"
}

DOOR = {
    "set": "[~] {p} carefully pushes a TNT minecart onto a closed door...",
    "disarm": "[=] {p2} break{s} {p}'s TNT minecart.",
    "escape": "[=] {p2} trigger{s} {p}'s TNT minecart, but survive{s} the explosion.",
    "kill": "[-] {p2} {w} blown up by {p}'s trapped door"
}

TYPES = [
    MINECART,
    FALL,
    LAVA,
    SKULK,
    OBSERVER,
    DOOR,
]
