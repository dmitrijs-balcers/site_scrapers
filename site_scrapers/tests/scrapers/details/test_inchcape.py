import unittest
import os

from returns.result import Success

from site_scrapers.models.Car import CarFull, CarDate
from site_scrapers.scrapers.details.inchcape import scrape_inchcape_car_detail

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class UtilsTestCase(unittest.TestCase):
    def test_tiguan_x6m(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_vw_tiguan.html")) as car:
            self.assertEqual(Success(CarFull(
                url='https://certified.inchcape.lv/auto/volkswagen/volkswagen-tiguan-2018-20-awd-110-kw-ford1-15102021154948',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/34148/6184fc2570830.jpg',
                summary='Volkswagen Tiguan 2018 2.0  AWD 110 kW, 102200 km',
                date=CarDate(month='03', year='2018'),
                type='SUV',
                transmission='Automātiskā',
                hp='110 kW',
                price=27990,
                vin='WVGZZZ5NZJW389548',
                registrationNo=None,
                mileage=102200,
                engineSize=None,
                techInspDate=None,
                fuelType='diesel',
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
                url='https://certified.inchcape.lv/auto/bmw/bmw-x6-m-2016-44-423-kw-f86-30393-02112021100237',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/34286/61a0aedb3807b.jpg',
                summary='BMW X6 M 2016 4.4   423 kW F86, 133543 km',
                date=CarDate(month='06', year='2016'),
                type='SUV',
                transmission='Automātiskā',
                hp='423 kW',
                price=54900,
                vin='WBSKW810100G93368',
                registrationNo=None,
                mileage=133543,
                engineSize=None,
                techInspDate=None,
                fuelType='petrol',
                body="suv",
                drivetrain='awd',
                color=None,
                hasWarranty=True,
                doors=None,
                country='lv',
                dealer='inchcape'
            )), scrape_inchcape_car_detail(car.read()))

    def test_ford_focus(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_ford_focus.html")) as car:
            self.assertEqual(Success(CarFull(
                url='https://certified.inchcape.lv/auto/ford/ford-focus-2016-10-fwd-92-kw-ford1-14092021144651',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/34066/61781015e92b9.jpg',
                summary='Ford Focus 2016 1.0  FWD 92 kW, 160247 km',
                date=CarDate(month='11', year='2016'),
                type='Hečbeks',
                transmission='Automātiskā',
                hp='92 kW',
                price=9990,
                vin='WF05XXGCC5GY15636',
                registrationNo=None,
                mileage=160247,
                engineSize=None,
                techInspDate=None,
                fuelType='petrol',
                body="hatchback",
                drivetrain='fwd',
                color=None,
                hasWarranty=True,
                doors=None,
                country='lv',
                dealer='inchcape'
            )), scrape_inchcape_car_detail(car.read()))

    def test_bmw_530(self) -> None:
        with open(os.path.join(THIS_FOLDER, "inchcape/inchcape_bmw_530.html")) as car:
            self.assertEqual(Success(CarFull(
                url='https://certified.inchcape.lv/auto/bmw/bmw-530-2019-20-rwd-135-kw-g30-iperformance-30393-05102021164152',
                previewImgSrc='https://certified.inchcape.lv/assets/images/auto/33944/61603d224f07d.jpg',
                summary='BMW 530 2019 2.0  RWD 135 kW G30 , Iperformance, 47522 km',
                date=CarDate(month='07', year='2019'),
                type='Sedans',
                transmission='Automātiskā',
                hp='135 kW',
                price=46800,
                vin='WBAJA910X0GF99601',
                registrationNo=None,
                mileage=47522,
                engineSize=None,
                techInspDate=None,
                fuelType="hybrid",
                body="sedan",
                drivetrain='rwd',
                color=None,
                hasWarranty=True,
                doors=None,
                country='lv',
                dealer='inchcape'
            )), scrape_inchcape_car_detail(car.read()))


if __name__ == '__main__':
    unittest.main()
