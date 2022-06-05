import unittest
import os

from returns.result import Success

from site_scrapers.models.Car import CarFull, CarDate
from site_scrapers.scrapers.details.inchcape import scrape_inchcape_car_detail

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class UtilsTestCase(unittest.TestCase):
    def test_lexus_ux(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_lexus_ux.html")) as car:
            self.assertEqual(Success(
                CarFull(
                    url='https://certified.inchcape.lv/auto/lexus/lexus-ux-jlr1-10052022145338',
                    previewImgSrc='https://certified.inchcape.lv/assets/images/auto/2450/627b8f3221975.jpg',
                    summary='Lexus UX 2019 2.0   112 kW Premium pluss, 19 500 km',
                    date=CarDate(month='00', year='2019'),
                    type='SUV',
                    transmission='Automātiskā',
                    hp='112 kW',
                    price=33900,
                    vin='JTHY65BH602032276',
                    registrationNo=None,
                    mileage=19500,
                    engineSize=1987,
                    techInspDate=None,
                    fuelType='hybrid',
                    body='suv',
                    drivetrain='fwd',
                    color=None,
                    hasWarranty=True,
                    doors=None,
                    country='lv',
                    dealer='inchcape',
                )), scrape_inchcape_car_detail(car.read()))

    def test_vw_tiguan(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_vw_tiguan.html")) as car:
            self.assertEqual(Success(CarFull(
                url='https://certified.inchcape.lv/auto/volkswagen/volkswagen-tiguan-ford1-07042022132402',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/2400/625830347fd60.jpg',
                summary='Volkswagen Tiguan 2017 2.0   132kw R-line, 71 400 km',
                date=CarDate(month='00', year='2017'),
                type='SUV',
                transmission='Automātiskā',
                hp='132kw',
                price=31900,
                vin='WVGZZZ5NZHW867620',
                registrationNo=None,
                mileage=71400,
                engineSize=1984,
                techInspDate=None,
                fuelType='petrol',
                body='suv',
                drivetrain='awd',
                color=None,
                hasWarranty=True,
                doors=None,
                country='lv',
                dealer='inchcape',
            )), scrape_inchcape_car_detail(car.read()))

    def test_bmw_x6m(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_bmw_x6m.html")) as car:
            self.assertEqual(Success(CarFull(
                url='https://certified.inchcape.lv/auto/bmw/bmw-x6-m-30393-02112021100237',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/2135/61a0aedb3807b.jpg',
                summary='BMW X6 M 2016 4.4   423 kW F86, 133 543 km',
                date=CarDate(month='00', year='2016'),
                type='SUV',
                transmission='Automātiskā',
                hp='423 kW',
                price=51900,
                vin='WBSKW810100G93368',
                registrationNo=None,
                mileage=133543,
                engineSize=4395,
                techInspDate=None,
                fuelType='petrol',
                body='suv',
                drivetrain='awd',
                color=None,
                hasWarranty=True,
                doors=None,
                country='lv',
                dealer='inchcape',
            )), scrape_inchcape_car_detail(car.read()))

    def test_ford_mondeo(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_ford_mondeo.html")) as car:
            self.assertEqual(Success(CarFull(
                url='https://certified.inchcape.lv/auto/ford/ford-mondeo-ford1-16022022132555',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/2176/620ce0ba75e2b.jpg',
                summary='Ford Mondeo 2017 2.0   180 hp TITANIUM, 76 203 km',
                date=CarDate(month='00', year='2017'),
                type='Universālis',
                transmission='Automātiskā',
                hp='180 hp',
                price=21590,
                vin='WF0FXXWPCFGA22145',
                registrationNo=None,
                mileage=76203,
                engineSize=1998,
                techInspDate=None,
                fuelType='diesel',
                body='wagon',
                drivetrain='fwd',
                color=None,
                hasWarranty=True,
                doors=None,
                country='lv',
                dealer='inchcape',
            )), scrape_inchcape_car_detail(car.read()))

    def test_bmw_530(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_bmw_530.html")) as car:
            self.assertEqual(Success(CarFull(
                url='https://certified.inchcape.lv/auto/bmw/bmw-530-30393-10032022144025',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/2196/6238615c304e0.jpg',
                summary='BMW 530 2018 2.0  AWD 185 kW i xDrive Luxury Line G31, 62 617 km',
                date=CarDate(month='00', year='2018'),
                type='Universālis',
                transmission='Automātiskā',
                hp='185 kW',
                price=37900,
                vin='WBAJL51010BL93144',
                registrationNo=None,
                mileage=62617,
                engineSize=1998,
                techInspDate=None,
                fuelType='petrol',
                body='wagon',
                drivetrain='awd',
                color=None,
                hasWarranty=True,
                doors=None,
                country='lv',
                dealer='inchcape'
            )), scrape_inchcape_car_detail(car.read()))


if __name__ == '__main__':
    unittest.main()
