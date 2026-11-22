import ipaddress


class IpInfo:
    """
    Classe représentant les informations d'une adresse IP publique (IPv4 ou IPv6).
    Respecte le principe d'encapsulation de la Programmation Orientée Objet (POO).
    """

    def __init__(self, ip, city="Inconnue", region="Inconnue", country="Inconnu", 
                 isp="Inconnu", timezone="Inconnu", lat=None, lon=None):
        """
        Initialise un nouvel objet IpInfo avec des attributs privés.
        """
        self.__ip = ip
        self.__version = self.__detect_ip_version(ip)
        self.__city = city
        self.__region = region
        self.__country = country
        self.__isp = isp
        self.__timezone = timezone
        self.__lat = lat
        self.__lon = lon

    def __detect_ip_version(self, ip_str):
        """
        Méthode privée pour détecter automatiquement si l'adresse est IPv4 ou IPv6.
        """
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            return f"IPv{ip_obj.version}"
        except ValueError:
            return "Format IP invalide"

    # --- Getters (Accesseurs) pour respecter l'encapsulation ---
    @property
    def ip(self):
        return self.__ip

    @property
    def version(self):
        return self.__version

    @property
    def city(self):
        return self.__city

    @property
    def region(self):
        return self.__region

    @property
    def country(self):
        return self.__country

    @property
    def isp(self):
        return self.__isp

    @property
    def timezone(self):
        return self.__timezone

    @property
    def coordinates(self):
        return (self.__lat, self.__lon)

    # --- Méthodes d'affichage et de conversion ---
    def to_dict(self):
        """
        Convertit l'objet en dictionnaire (utile pour un export JSON).
        """
        return {
            "ip": self.__ip,
            "version": self.__version,
            "city": self.__city,
            "region": self.__region,
            "country": self.__country,
            "isp": self.__isp,
            "timezone": self.__timezone,
            "latitude": self.__lat,
            "longitude": self.__lon
        }

    def __str__(self):
        """
        Formate l'affichage de l'objet lorsque l'on fait print(objet_ip).
        """
        return (
            f"\n=== Informations Adresse IP ({self.__version}) ===\n"
            f"Adresse IP   : {self.__ip}\n"
            f"Localisation : {self.__city}, {self.__region} ({self.__country})\n"
            f"Fournisseur  : {self.__isp}\n"
            f"Fuseau hor.  : {self.__timezone}\n"
            f"Coordonnées  : {self.__lat}, {self.__lon}\n"
            f"=========================================="
        )


# Bloc de test unitaire (exécuté quand on lance directement ce fichier)
if __name__ == "__main__":
    test_ipv4 = IpInfo("8.8.8.8", "Mountain View", "California", "United States", "Google LLC", "America/Los_Angeles", 37.386, -122.0838)
    print(test_ipv4)

    test_ipv6 = IpInfo("2001:4860:4860::8888", "Mountain View", "California", "United States", "Google LLC")
    print(test_ipv6)
