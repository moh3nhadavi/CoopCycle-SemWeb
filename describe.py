from rdflib import Graph, Namespace, RDF, Literal, SDO, URIRef, XSD, BNode
import questionary


    
    
def describe_data():
    wd = Namespace("http://www.wikidata.org/entity/")
    ex = Namespace("http://www.example.org/#")

    g = Graph()
    g.bind('wd', wd)
    g.bind('ex', ex)

    # Ask questions
    questionary.print("Please answer the following questions to describe your preferences:")
    # Personal information
    questionary.print("First Some questions about you:")
    name = questionary.text("Please write your full name").ask()
    postal_code = questionary.text("Please write your postal code:").ask()
    locality = questionary.text("Please write your locality:").ask()
    
    # Food preferences
    questionary.print("Now some questions about your food preferences:")
    restaurant_uri = questionary.text("Please write the restaurant uri that you seek:").ask()
    delivery_max_price = questionary.text("What is your maximum delivery price in EUR:").ask()
    
    # location
    questionary.print("Now some questions about your location:")
    geoLocation = questionary.text("where do you live? Provide an answer of the form longitude,latitude.").ask()
    latitude = geoLocation.split(",")[0]
    longitude = geoLocation.split(",")[1]
    max_distance = questionary.text("Please provide your maximum distance").ask()
    

    user = ex[name.replace(" ", "_")]
    Baddress = BNode()
    Bseek = BNode()
    Bprice = BNode()
    BavailableAtOrFrom = BNode() 
    BgeoWithin = BNode()
    BgeoMidpoint = BNode()
       

    # Add data
    # user detail
    g.add((user, RDF.type, SDO.Person))
    g.add((user, SDO.name, Literal(name)))
    # user address
    g.add((user, SDO.address, Baddress))
    g.add((Baddress, RDF.type, SDO.PostalAddress))
    g.add((Baddress, SDO.postalCode, Literal(postal_code)))
    g.add((Baddress, SDO.addressLocality, Literal(locality)))
    # user preference
    g.add((user, SDO.seeks, Bseek))
    g.add((Bseek, SDO.seller, URIRef(restaurant_uri)))
    g.add((Bseek, SDO.priceSpecification, Bprice))
    g.add((Bprice, SDO.maxPrice, Literal(delivery_max_price, datatype=XSD.float)))
    g.add((Bprice, SDO.priceCurrency, Literal("EUR")))
    # user location
    g.add((Bseek, SDO.availableAtOrFrom, BavailableAtOrFrom))
    g.add((BavailableAtOrFrom, SDO.geoWithin, BgeoWithin))
    g.add((BgeoWithin, RDF.type, SDO.GeoShape))
    g.add((BgeoWithin, SDO.geoMidpoint, BgeoMidpoint))
    g.add((BgeoMidpoint, SDO.latitude, Literal(latitude, datatype=XSD.float)))
    g.add((BgeoMidpoint, SDO.longitude, Literal(longitude, datatype=XSD.float)))
    g.add((BgeoWithin, SDO.geoRadius, Literal(max_distance, datatype=XSD.float)))
    

    # Serialize and save
    filename = name.replace(" ","_") + "-preference.ttl"
    with open(filename, 'w', encoding='utf-8') as w:
        w.write(g.serialize(format="turtle"))