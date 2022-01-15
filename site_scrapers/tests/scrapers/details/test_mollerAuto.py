import unittest
import os

from returns.result import Success

from site_scrapers.models.Car import CarFull, CarDate
from site_scrapers.scrapers.details.mollerAuto import scrape_moller_car_detail

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class UtilsTestCase(unittest.TestCase):
    def test_audi(self) -> None:
        with open(os.path.join(THIS_FOLDER, "moller_data/moller_audi.html")) as car:
            self.assertEqual(Success(CarFull(
                url="https://lietotiauto.mollerauto.lv/lv/vehicle/10236564",
                previewImgSrc='https://lietotiauto.mollerauto.lv/lv/vehicle/simage/10237323/10237323.jpg',
                summary='Audi A4 2.0 TFSI 110kw aut. 2.0 110kW aut',
                date=CarDate("07", "2020"),
                type='sedans',
                transmission='automātiskā',
                hp='150 ZS (110 kW)',
                price=33600,
                vin='WAUZZZF43LA059292',
                registrationNo='MN6786',
                mileage=20910,
                engineSize=2000,
                techInspDate=CarDate("07", "2022"),
                fuelType="petrol",
                body="sedan",
                drivetrain=None,
                color='melna',
                hasWarranty=True,
                doors='4/5',
                country="lv",
                dealer="moller-auto"
            )), scrape_moller_car_detail(car.read()))

    def test_audi_a6_sport(self) -> None:
        with open(os.path.join(THIS_FOLDER, "moller_data/moller_audi_a6_sport.html")) as car:
            self.assertEqual(Success(CarFull(
                url="https://lietotiauto.mollerauto.lv/lv/vehicle/10236087",
                previewImgSrc='https://lietotiauto.mollerauto.lv/lv/vehicle/simage/10236092/10236092.jpg',
                summary='Audi A6 Sport 2.0 150kW aut',
                date=CarDate("05", "2021"),
                type='universāls',
                transmission='automātiskā',
                hp='204 ZS (150 kW)',
                price=62600,
                vin='WAUZZZF22MN086735',
                registrationNo='086735',
                mileage=9019,
                engineSize=2000,
                techInspDate=CarDate("05", "2024"),
                fuelType="diesel",
                body="wagon",
                drivetrain="awd",
                color='cita',
                hasWarranty=True,
                doors='4/5',
                country="lt",
                dealer="moller-auto"
            )), scrape_moller_car_detail(car.read()))

    def test_vw_amarok(self) -> None:
        with open(os.path.join(THIS_FOLDER, "moller_data/moller_vw_amarok.html")) as car:
            self.assertEqual(Success(CarFull(
                url="https://lietotiauto.mollerauto.lv/lv/vehicle/10235196",
                previewImgSrc='https://lietotiauto.mollerauto.lv/lv/vehicle/simage/10236919/10236919.jpg',
                summary='Volkswagen Amarok 2.0 106kW meh',
                date=CarDate("12", "2010"),
                type='pikaps',
                transmission='mehāniskā',
                hp='144 ZS (106 kW)',
                price=16490,
                vin='WV1ZZZ2HZB8024645',
                registrationNo='847KGR',
                mileage=133710,
                engineSize=2000,
                techInspDate=CarDate("12", "2021"),
                fuelType="diesel",
                body="pickup",
                drivetrain="awd",
                color='pelēka',
                hasWarranty=None,
                doors='4/5',
                country="ee",
                dealer="moller-auto"
            )), scrape_moller_car_detail(car.read()))

if __name__ == '__main__':
    unittest.main()
