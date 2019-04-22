# wireless-individual-encryption

The Wireless Individual Encryption protocol, created and designed by Artem Sviridov
aims to become a standard security protocol for establishing encrypted communication
and identificationbetween internet access points and personal computers in online
communication. The usage of WIE technology ensures that all data transmitted between
the access point and the computer remains encrypted. The need for this is evident in
the wide use of open wifi networks. Our engineering approach is to authenticate true
wifi networks with a Certificate Authority. The list of trusted wifis will be held on
the device, and when a new wifi is found WIE will check if this new wifi has been
certified by the CA server.
