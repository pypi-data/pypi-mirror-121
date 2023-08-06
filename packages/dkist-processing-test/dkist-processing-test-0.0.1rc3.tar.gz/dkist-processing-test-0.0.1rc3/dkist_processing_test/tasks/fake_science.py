"""
Fake science task
"""
from uuid import uuid4

from astropy.io import fits
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import ScienceTaskL0ToL1Base


class GenerateCalibratedData(ScienceTaskL0ToL1Base):
    def run(self):
        for path, hdu in self.fits_data_read_hdu(tags=Tag.input()):
            header = hdu.header
            data = hdu.data
            output_hdu = fits.PrimaryHDU(data=data, header=header)
            output_hdul = fits.HDUList([output_hdu])
            self.fits_data_write(
                hdu_list=output_hdul,
                tags=[Tag.calibrated(), Tag.frame(), Tag.stokes("I")],
            )


class GenerateL1OutputData(ScienceTaskL0ToL1Base):
    def run(self):
        number_of_frames = len(list(self.read(tags=Tag.input())))
        count = 0
        for path, hdu in self.fits_data_read_hdu(tags=Tag.input()):
            header = hdu.header
            data = hdu.data
            # Change frame id for frame inventory
            header["FILE_ID"] = uuid4().hex
            header["DATE-END"] = header["DATE-BEG"]
            # ADD DATA CENTER HEADERS (ONLY IF GUARANTEED TO EXIST)
            header["DSETID"] = self.dataset_id
            header["POINT_ID"] = self.dataset_id
            header["FRAMEVOL"] = round(float(hdu.size / 1000000), 2)
            header["PROCTYPE"] = "L1"
            header["RRUNID"] = self.recipe_run_id
            header["RECIPEID"] = self.metadata_store_recipe_id
            header["RINSTID"] = self.metadata_store_recipe_instance_id
            header["EXTNAME"] = "observation"
            header["SOLARNET"] = 0.5
            header["OBS_HDU"] = 1
            # ADD DATASET HEADERS (ONLY IF GUARANTEED TO EXIST)
            header["DNAXIS"] = 3
            header["DNAXIS1"] = header["NAXIS1"]
            header["DNAXIS2"] = header["NAXIS2"]
            header["DNAXIS3"] = number_of_frames
            header["DTYPE1"] = "SPATIAL"
            header["DTYPE2"] = "SPATIAL"
            header["DTYPE3"] = "TEMPORAL"
            header["DPNAME1"] = "spatial x"
            header["DPNAME2"] = "spatial y"
            header["DPNAME3"] = "frame number"
            header["DWNAME1"] = "helioprojective longitude"
            header["DWNAME2"] = "helioprojective latitude"
            header["DWNAME3"] = "time"
            header["DUNIT1"] = "arcsec"
            header["DUNIT2"] = "arcsec"
            header["DUNIT3"] = "s"
            header["DAAXES"] = 2
            header["DEAXES"] = 1
            header["DINDEX3"] = count
            header["LINEWAV"] = header["WAVELNTH"]
            header["FRAMEWAV"] = header["WAVELNTH"]
            header["LEVEL"] = 1
            file_name = self.format_l1_file_name(header)
            header["FILENAME"] = file_name
            header["CALVERS"] = "version string"
            header["CAL_URL"] = "url string"
            header["HEADVERS"] = "version string"
            header["HEAD_URL"] = "url string"
            header["INFO_URL"] = "url string"

            header["WAVEMIN"] = 1.0
            header["DATE-AVG"] = header["DATE-OBS"]
            header["DATEREF"] = header["DATE-OBS"]
            header["OBSGEO-X"] = 0.0
            header["OBSGEO-Y"] = 0.0
            header["OBSGEO-Z"] = 0.0
            header["NBIN"] = 1
            header["TELAPSE"] = 10.0
            header["WAVEREF"] = "Air"
            header["WAVEUNIT"] = -9
            header["NBIN2"] = 1
            header["OBS_VR"] = 0.0
            header["NBIN1"] = 1
            header["WAVEMAX"] = 10.0
            header["NBIN3"] = 1
            header["BTYPE"] = "Data array"
            header["SPECSYS"] = "specsys"
            header["VELOSYS"] = True

            output_hdu = fits.PrimaryHDU(data=data, header=header)
            output_hdul = fits.HDUList([output_hdu])
            self.fits_data_write(
                hdu_list=output_hdul, tags=[Tag.output(), Tag.frame()], relative_path=file_name
            )
            count += 1
        movie_path = f"{self.dataset_id}_movie.mpg"
        self.write(b"Movie", tags=[Tag.output(), Tag.movie()], relative_path=movie_path)

    @staticmethod
    def format_l1_file_name(header: fits.Header, is_compressed: bool = False) -> str:
        stem = f"L1_{header['FILE_ID']}"
        if is_compressed:
            return f"{stem}.fitsz"
        return f"{stem}.fits"
