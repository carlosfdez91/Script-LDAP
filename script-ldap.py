# -*- coding: utf-8 -*-
import json
import ldap
import ldap.modlist as modlist
import getpass

#Abrimos el fichero json y lo cargamos
personas = open("humanos.json")
datos = json.load(personas)

#Solicitamos la password del admin de LDAP
password = getpass.getpass("Introduce la contraseña del admin de LDAP: ")

#Realizamos la conexion al servidor de ldap
uri = ldap.initialize("ldap://piolin.carlosfernandez.gonzalonazareno.org:389")
uri.simple_bind_s("cn=admin,dc=carlosfernandez,dc=gonzalonazareno,dc=org",password)

uidNumber = 2010
gidNumber = 2001

for i in datos["humanos"]:
        dn="uid=%s,ou=People,dc=carlosfernandez,dc=gonzalonazareno,dc=org" % str(i["usuario"])
        attrs = {}
        attrs['objectclass'] = ['top','posixAccount','inetOrgPerson','ldapPublicKey']
        attrs['cn'] = str(i["nombre"])
        attrs['uid'] = str(i["usuario"])
        attrs['sn'] = str(i["apellidos"])
        attrs['uidNumber'] = str(uidNumber)
        attrs['gidNUmber'] = str(gidNumber)
        attrs['mail'] = str(i["correo"])
        attrs['sshPublicKey'] = "ssh-rsa" + str(i["clave"])
        attrs['homeDirectory'] = ['/home/%s' % (str(i["usuario"]))]
        attrs['loginShell'] = ['/bin/bash']
        ldif = modlist.addModlist(attrs)
        uri.add_s(dn,ldif)
        uidNumber = uidNumber + 1

uri.unbind_s()
personas.close()
