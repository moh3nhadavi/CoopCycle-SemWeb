from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, RDFS, XSD, SDO

data = b'''
{
    "@context": "http://schema.org",
    "@id": "/api/restaurants/30",
    "@type": "http://schema.org/Restaurant",
    "name": "Mealk",
    "address": {
        "@id": "/api/addresses/2920",
        "@type": "http://schema.org/PostalAddress",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 49.875537,
            "longitude": 2.277711
        },
        "streetAddress": "14 Avenue Paul Claudel, 80000 Amiens, France",
        "telephone": "+33322724071",
        "name": "Mealk"
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "opens": "10:30",
            "closes": "14:45",
            "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ]
        },
        {
            "@type": "OpeningHoursSpecification",
            "opens": "18:00",
            "closes": "19:00",
            "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday"
            ]
        }
    ],
    "image": "https://beefast.coopcycle.org/media/cache/restaurant_thumbnail/62/3c/623c3c947b9c6.jpeg",
    "sameAs": "http://www.mealk.fr/",
    "description": "Mealk vous propose une cantine du midi, \u00e9picerie & fromagerie avec un maximum de produits bio & locaux avec pour base des produits laitiers sublim\u00e9s par une cuisine de savoir faire et de tradition. \r\n\r\nLa carte est \u00e9volutive en fonction des saisons !",
    "potentialAction": {
        "@type": "OrderAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://beefast.coopcycle.org/fr/restaurant/30-mealk",
            "inLanguage": "fr",
            "actionPlatform": [
                "http://schema.org/DesktopWebPlatform"
            ]
        },
        "deliveryMethod": [
            "http://purl.org/goodrelations/v1#DeliveryModeOwnFleet"
        ],
        "priceSpecification": {
            "@type": "DeliveryChargeSpecification",
            "appliesToDeliveryMethod": "http://purl.org/goodrelations/v1#DeliveryModeOwnFleet",
            "priceCurrency": "EUR",
            "price": "3.50",
            "eligibleTransactionVolume": {
                "@type": "PriceSpecification",
                "priceCurrency": "EUR",
                "price": "8.90"
            }
        }
    }
}
'''
data = data.replace(b"\r\n", b"\\n")
g = Graph()
# schema = Namespace("http://schema.org/")
g.parse(data=data, format="json-ld")
output_text = g.serialize(format="turtle")
output_text = output_text.replace("schema1", "schema")
with open('test.ttl', 'w') as f:
        f.write(output_text)