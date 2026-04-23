import googlemaps

from config import GOOGLE_MAPS_API_KEY
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def find_nearby_therapists_by_location(location: str) -> str:
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        return f"Sorry, I couldn't find the location '{location}'. Please try a different location."

    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    places_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=5000,
        type='health' ,
        keyword='therapist OR psychologist OR counselor'
    )
    top_5_places = places_result.get('results', [])[:5]
    therapists = []
    for place in top_5_places:
        name = place.get('name',"Unknown Therapist")
        address = place.get('vicinity',"Address not available")
        details = gmaps.place(place_id=place['place_id'], fields=['formatted_phone_number', 'website'])
        phone = details['result'].get('formatted_phone_number', 'Phone not available')
        therapists.append(f"{name} - {address} - {phone}")

    if not therapists:
        return f"Sorry, I couldn't find any therapists near '{location}'. Please try a different location."

    return "Here are some therapists near you:\n" + "\n".join(therapists)


print(find_nearby_therapists_by_location("Bangalore"))