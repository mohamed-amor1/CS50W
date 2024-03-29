# Generated by Django 4.2.1 on 2023-05-12 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_listing_comment_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Fashion", "Fashion"),
                    ("Toys", "Toys"),
                    ("Electronics", "Electronics"),
                    ("Home", "Home"),
                    ("Books", "Books"),
                    ("Sports", "Sports"),
                    ("Collectibles", "Collectibles"),
                    ("Art", "Art"),
                    ("Jewelry", "Jewelry"),
                    ("Antiques", "Antiques"),
                    ("Vehicles", "Vehicles"),
                    ("Instruments", "Musical Instruments"),
                    ("Tools", "Tools"),
                    ("Appliances", "Appliances"),
                    ("Beauty", "Beauty Products"),
                    ("Gaming", "Gaming Consoles & Video Games"),
                    ("Coins", "Coins & Currency"),
                    ("Tickets", "Event Tickets"),
                    ("Other", "Other"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
