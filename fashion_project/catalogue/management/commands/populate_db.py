import random
from django.core.management.base import BaseCommand
from faker import Faker
from catalogue.models import Designer, Trend, Garment

class Command(BaseCommand):
    help = "Remplit la base de données avec de fausses données de mode"

    def handle(self, *args, **kwargs):
        fake = Faker(['fr_FR', 'en_US']) 
        
        self.stdout.write("Suppression des anciennes données...")
        Garment.objects.all().delete()
        Designer.objects.all().delete()
        Trend.objects.all().delete()

        self.stdout.write("Création des données...")

        designers = []
        for _ in range(10):
            d = Designer.objects.create(
                name=fake.company(),
                country=fake.country(),
                founded_year=random.randint(1900, 2020)
            )
            designers.append(d)

        trends = []
        trend_names = ["Vintage", "Streetwear", "Minimaliste", "Luxe", "Sportswear", "Bohème"]
        for name in trend_names:
            t = Trend.objects.create(name=name, description=fake.text())
            trends.append(t)

        materials = ["Soie", "Coton", "Cuir", "Denim", "Velours", "Lin"]
        types = ["Robe", "Pantalon", "Veste", "Chemise", "Sac", "Chaussures"]

        for i in range(200):
            nom_vetement = f"{random.choice(types)} {fake.color_name()}"
            
            g = Garment.objects.create(
                name=nom_vetement.capitalize(),
                sku=f"REF-{random.randint(1000, 9999)}-{i}",
                price=random.uniform(20.0, 5000.0), # Prix entre 20 et 5000
                description=fake.paragraph(),
                stock_quantity=random.randint(0, 100),
                release_date=fake.date_between(start_date='-5y', end_date='today'),
                is_sustainable=fake.boolean(chance_of_getting_true=30),
                designer=random.choice(designers), # On pioche un designer au hasard
                cover_image_url=f"https://loremflickr.com/320/240/fashion?lock={i}" # Image aléatoire de mode
            )
            
            g.trends.set(random.sample(trends, k=random.randint(1, 2)))

        self.stdout.write(self.style.SUCCESS("Terminé ! 200 vêtements créés avec succès."))