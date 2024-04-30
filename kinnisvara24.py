import requests

url = "https://kinnisvara24.ee/search"
RUN = True
search_obj = {
    "hash": None,
    "addresses": [
        {
            "A1": "Tartu maakond",
            "A2": "Tartu linn",
        },
    ],
    "area_min": None,
    "area_max": None,
    "land_area_min": None,
    "land_area_max": None,
    "around_point": None,
    "bounds": [],
    "broker_id": None,
    "bureau_id": None,
    "build_year_min": None,
    "build_year_max": None,
    "client_day_date_max": None,
    "client_day_date_min": None,
    "comforts": [],
    "commercial_types": [],
    "deal_types": ["rent"],
    "developments_only": False,
    "energy_classes": [],
    "exclusives": False,
    "uniques": False,
    "extras": [],
    "floor_min": None,
    "floor_max": None,
    "from_owner": False,
    "with_detail_planning_only": False,
    "with_building_permit_only": False,
    "with_360_tour_only": False,
    "with_video_only": False,
    "intended_uses": [],
    "keywords": [],
    "materials": [],
    "object_types": ["apartment"],
    "price_max": None,
    "price_min": None,
    "price_per_m2_max": None,
    "price_per_m2_min": None,
    "land_price_per_m2_max": None,
    "land_price_per_m2_min": None,
    "water_supplies": [],
    "heating_types": [],
    "energy_sources": [],
    "rooms_max": None,
    "rooms_min": None,
    "sewage_types": [],
    "sort_by": "relevance",
    "sort_order": "desc",
    "page": 1,
    "utility_join_fees_paid": False,
    "has_repairs_canal": False,
    "is_development_lot": False,
    "is_top_floor": False,
    "has_water_border": False,
    "pets_allowed": False,
    "with_usage_permit": False,
    "has_client_day": False,
    "free": False,
    "amount": None,
    "rooms": None,
    "period": None,
    "has_furniture": None,
    "has_washing": False,
    "are_pets_allowed": False,
    "show_deactivated": False,
    "price_without_utilities": False,
    "has_kitchen": False,
    "has_job_possibility": False,
    "additional": [],
    "house_part_types": [],
    "conditions": [],
    "neighbours": [],
    "road_conditions": [],
    "address": [],
}

full_data = []
while RUN:
    z = requests.post(url, json=search_obj)

    if len(z.json()["data"]) == 0:
        RUN = False
    else:
        for d in z.json()["data"]:

            # More info can be extracted with more attributes

            full_data.append({
                "price": d["hind"],
                "area": d["area"],
                "rooms": d["rooms"],
                "permalink": d["permalink"],
            })

            """
            Format:
                price
                area
                rooms
                submitted
                permalink
            """
    search_obj["page"] += 1
print(full_data)
