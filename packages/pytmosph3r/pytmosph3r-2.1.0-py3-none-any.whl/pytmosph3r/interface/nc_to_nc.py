from pytmosph3r import DiagfiModel
from .netcdf import ncOutput
from pytmosph3r.atmosphere import AltitudeAtmosphere
# from pytmosph3r.model import DiagfiModel

def nc_to_nc():
    """Utility tool to rewrite a diagfi.nc.
    """
    import argparse
    import pathlib
    import json

    parser = argparse.ArgumentParser(description='diagfi-to-hdf5-converter')
    parser.add_argument("-i","--input",dest="input",type=str,required=True,help="Input diagfi filename")
    parser.add_argument("-r", "--radius-scale", dest='radius_scale', default=1, type=float, help="Change the scale of the radius of the planet when saving .nc (for visual reasons).")
    parser.add_argument("-p", "--min-pressure", dest='min_pressure', type=float, default=1e-5,help="Top pressure.")
    parser.add_argument("-o","--output",dest="output",type=str,required=True,help="Output netCDF filename")
    parser.add_argument('-g', '--gas-dict', default="{}", type=json.loads, help="Example: {\\\"H2O\\\":\\\"h2o_vap\\\"}")
    args=parser.parse_args()

    # gas_dict = json.loads(args.gas_dict)
    gas_dict = args.gas_dict
    model = DiagfiModel(filename=args.input)
    model.read_data(gas_dict=gas_dict)
    model.input_atmosphere.build(model)
    model.input_atmosphere.compute_altitude()
    model.n_vertical = model.input_atmosphere.n_vertical
    model.input_atmosphere.min_pressure = args.min_pressure
    model.interp = 'linear'
    model.gas_dict = None
    model.aerosols_dict = None
    model.atmosphere = AltitudeAtmosphere(model)
    model.atmosphere.build()

    with ncOutput(args.output) as nc:
        nc.write_model(model, radius_scale=args.radius_scale)

if __name__ == "__main__":
    nc_to_nc()