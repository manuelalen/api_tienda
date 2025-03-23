import dlt

@dlt.view(name="characters")
def load_characters():
    return spark.read.table("workspace.starwars.characters")

@dlt.view(name="planets")
def load_planets():
    return spark.read.table("workspace.starwars.planets")

@dlt.view(name="species")
def load_species():
    return spark.read.table("workspace.starwars.species")

@dlt.table(name="starwars_combined")
def combine_characters_with_planets_and_species():
    characters = dlt.read("characters")
    planets = dlt.read("planets")
    species = dlt.read("species")

    return (
        characters
        .join(planets, characters["homeworld"] == planets["name"], "left")
        .join(species, characters["species"] == species["name"], "left")
        .select(
            characters["name"].alias("character_name"),
            planets["name"].alias("planet_name"),
            planets["climate"],
            species["name"].alias("species_name"),
            species["language"]
        )
    )
