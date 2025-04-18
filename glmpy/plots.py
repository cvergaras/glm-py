import netCDF4
import numpy as np
import pandas as pd
import numpy.ma as ma
import matplotlib.dates as mdates

from typing import Union, List
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.image import AxesImage
from datetime import datetime, timedelta



class LakePlotter:
    """Common plots for the `lake.csv` output.
    
    Creates time series plots of lake characteristics (e.g., volume, 
    temperature, heat fluxes, etc.) on provided matplotlib `Axes` objects. 
    Reads daily lake measurement data from the `lake.csv` file generated by 
    running a GLM simulation.
    
    Examples
    --------
    Plot the lake volume (m^3):

    >>> from glmpy import plots
    >>> import matplotlib.pyplot as plt
    >>> lake = plots.LakePlotter("lake.csv")
    >>> fig, ax = plt.subplots()
    >>> lake.lake_volume(ax)
    >>> plt.show()
    
    Change the line colour by providing a dictionary of matplotlib `plot` 
    parameters:

    >>> lake = plots.LakePlotter("lake.csv")
    >>> fig, ax = plt.subplots()
    >>> lake.lake_volume(ax, {"color": "red"})
    >>> plt.show()
    """

    def __init__(self, lake_csv_path: str):
        """Initialise the LakePlotter with the `lake.csv` file.

        Parameters
        ----------
        lake_csv_path : str
            Path to the `lake.csv` file generated by GLM
        """
        self._lake_csv = pd.read_csv(lake_csv_path)
        days = [date.split(" ")[0] for date in list(self._lake_csv["time"])]
        self._x_dates = [
            datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
            for date in days
        ]
        self._date_formatter = mdates.DateFormatter("%d/%m/%y")

    def _set_default_plot_params(
        self, param_dict: Union[dict, None], defaults_dict: dict
    ):
        if isinstance(param_dict, dict):
            for key, value in defaults_dict.items():
                if key not in param_dict:
                    param_dict[key] = value

    def lake_volume(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        """
        Lake volume.

        Line plot of the lake volume (m^3).

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        param_dict: dict
            Plotting parameters that will be passed to
            `matplotlib.axes.Axes.plot`.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self._x_dates),
            self._lake_csv["Volume"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake volume ($\mathregular{m}^{3}$)")
        ax.set_xlabel("Date")
        return out

    def lake_level(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        """
        Lake surface height.

        Line plot of the lake level (m).

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        param_dict: dict
            Plotting parameters that will be passed to
            `matplotlib.axes.Axes.plot`.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self._x_dates),
            self._lake_csv["Lake Level"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake surface height (m)")
        ax.set_xlabel("Date")
        return out

    def lake_surface_area(
        self, ax: Axes, param_dict: dict = {}
    ) -> List[Line2D]:
        """Lake surface area.

        Line plot of the lake surface area (m^2).

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        param_dict: dict
            Plotting parameters that will be passed to
            `matplotlib.axes.Axes.plot`.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self._x_dates),
            self._lake_csv["Surface Area"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake surface area ($\mathregular{m}^{2}$)")
        ax.set_xlabel("Date")
        return out

    def water_balance(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        """Lake water balance.

        Line plot of the net water balance (m^3/day). Calculated by:
        `Rain + Snowfall + Local Runoff + Tot Inflow Vol + Evaporation -
        Tot Outflow Vol`.

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        param_dict: dict
            Plotting parameters that will be passed to
            `matplotlib.axes.Axes.plot`.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        self._lake_csv["water_balance"] = (
            self._lake_csv["Rain"]
            + self._lake_csv["Snowfall"]
            + self._lake_csv["Local Runoff"]
            + self._lake_csv["Tot Inflow Vol"]
            + self._lake_csv["Evaporation"]
            - self._lake_csv["Tot Outflow Vol"]
        )
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self._x_dates),
            self._lake_csv["water_balance"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel(
            "Total flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)"
        )
        ax.set_xlabel("Date")
        return out

    def water_balance_components(
        self,
        ax: Axes,
        tot_inflow_vol_params: Union[dict, None] = {},
        tot_outflow_vol_params: Union[dict, None] = {},
        overflow_vol_params: Union[dict, None] = {},
        evaporation_params: Union[dict, None] = {},
        rain_params: Union[dict, None] = {},
        local_runoff_params: Union[dict, None] = {},
        snowfall_params: Union[dict, None] = {},
    ) -> List[Line2D]:
        """
        Lake water balance components.

        Daily line plot of the water balance components (m^3/day):
            - Total inflow
            - Total outflow
            - Overflow
            - Evaporation
            - Rain
            - Local runoff
            - Snowfall

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        tot_inflow_vol_params: Union[dict, None]
            Plotting parameters for `Tot Inflow Vol`. If `None`, nothing
            will be plotted. Default is {}.
        tot_outflow_vol_params: Union[dict, None]
            Plotting parameters for `Tot Outflow Vol`. If `None`, nothing
            will be plotted. Default is {}.
        overflow_vol_params: Union[dict, None]
            Plotting parameters for `Overflow Vol`. If `None`, nothing
            will be plotted. Default is {}.
        evaporation_params: Union[dict, None]
            Plotting parameters for `Evaporation`. If `None`, nothing
            will be plotted. Default is {}.
        rain_params: Union[dict, None]
            Plotting parameters for `Rain`. If `None`, nothing
            will be plotted. Default is {}.
        local_runoff_params: Union[dict, None]
            Plotting parameters for `Local Runoff`. If `None`, nothing
            will be plotted. Default is {}.
        snowfall_params: Union[dict, None]
            Plotting parameters for `Snowfall`. If `None`, nothing
            will be plotted. Default is {}.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        plot_params = [
            tot_inflow_vol_params,
            tot_outflow_vol_params,
            overflow_vol_params,
            evaporation_params,
            rain_params,
            local_runoff_params,
            snowfall_params,
        ]
        default_params = [
            {"color": "#1f77b4", "label": "Total inflow"},
            {"color": "#d62728", "label": "Total outflow"},
            {"color": "#9467bd", "label": "Overflow"},
            {"color": "#ff7f0e", "label": "Evaporation"},
            {"color": "#2ca02c", "label": "Rain"},
            {"color": "#17becf", "label": "Local runoff"},
            {"color": "#7f7f7f", "label": "Snowfall"},
        ]
        for i in range(len(plot_params)):
            self._set_default_plot_params(plot_params[i], default_params[i])
        out = []
        components = [
            ("Tot Inflow Vol", tot_inflow_vol_params),
            ("Tot Outflow Vol", tot_outflow_vol_params),
            ("Overflow Vol", overflow_vol_params),
            ("Evaporation", evaporation_params),
            ("Rain", rain_params),
            ("Local Runoff", local_runoff_params),
            ("Snowfall", snowfall_params),
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                if column_name == "Tot Outflow Vol":
                    (out_component,) = ax.plot(
                        mdates.date2num(self._x_dates),
                        -self._lake_csv[column_name],
                        **param_dict,
                    )
                else:
                    (out_component,) = ax.plot(
                        mdates.date2num(self._x_dates),
                        self._lake_csv[column_name],
                        **param_dict,
                    )
                out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Flux ($\mathregular{m}^{3}$ $\mathregular{day}^{-1}$)")
        ax.set_xlabel("Date")
        return out

    def heat_balance_components(
        self,
        ax,
        daily_qsw_params: Union[dict, None] = {},
        daily_qe_params: Union[dict, None] = {},
        daily_qh_params: Union[dict, None] = {},
        daily_qlw_params: Union[dict, None] = {},
    ) -> List[Line2D]:
        """
        Lake heat fluxes.

        Daily line plot of four heat balance components (W/m^2):
            - Mean shortwave radiation
            - Mean latent heat
            - Mean sensible heat
            - Mean longwave radiation

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        daily_qsw_params: Union[dict, None]
            Plotting parameters for `Daily Qsw`. If `None`, nothing
            will be plotted. Default is {}.
        daily_qe_params: Union[dict, None]
            Plotting parameters for `Daily Qe`. If `None`, nothing
            will be plotted. Default is {}.
        daily_qh_params: Union[dict, None]
            Plotting parameters for `Daily Qh`. If `None`, nothing
            will be plotted. Default is {}.
        daily_qlw_params: Union[dict, None]
            Plotting parameters for `Daily Qlw`. If `None`, nothing
            will be plotted. Default is {}.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        plot_params = [
            daily_qsw_params,
            daily_qe_params,
            daily_qh_params,
            daily_qlw_params,
        ]
        default_params = [
            {"color": "#1f77b4", "label": "Mean shortwave radiation"},
            {"color": "#d62728", "label": "Mean latent heat"},
            {"color": "#2ca02c", "label": "Mean sensible heat"},
            {"color": "#ff7f0e", "label": "Mean longwave radiation"},
        ]
        for i in range(len(plot_params)):
            self._set_default_plot_params(plot_params[i], default_params[i])
        out = []
        components = [
            ("Daily Qsw", daily_qsw_params),
            ("Daily Qe", daily_qe_params),
            ("Daily Qh", daily_qh_params),
            ("Daily Qlw", daily_qlw_params),
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                (out_component,) = ax.plot(
                    mdates.date2num(self._x_dates),
                    self._lake_csv[column_name],
                    **param_dict,
                )
                out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Heat flux ($\mathregular{W}$/$\mathregular{m}^{2}$)")
        ax.set_xlabel("Date")
        return out

    def surface_temp(self, ax: Axes, param_dict: dict = {}) -> List[Line2D]:
        """Lake surface temperature.

        Line plot of the lake surface temperature (celsius).

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        param_dict: dict
            Plotting parameters that will be passed to
            `matplotlib.axes.Axes.plot`.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        self._set_default_plot_params(param_dict, {"color": "#1f77b4"})
        out = ax.plot(
            mdates.date2num(self._x_dates),
            self._lake_csv["Surface Temp"],
            **param_dict,
        )
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake surface temperature (°C)")
        ax.set_xlabel("Date")
        return out

    def lake_temp(
        self,
        ax: Axes,
        min_temp_params: Union[dict, None] = {},
        max_temp_params: Union[dict, None] = {},
    ) -> List[Line2D]:
        """Min./max. temperature within lake.

        Line plot of the minimum and maximum temperature (celsius) within the
        lake.

        Parameters
        ----------
        ax: Axes
            The matplotlib Axes that the data will be plotted on.
        min_temp_params: Union[dict, None]
            Plotting parameters for `Min Temp`. If `None`, nothing
            will be plotted. Default is {}.
        max_temp_params: Union[dict, None]
            Plotting parameters for `Max Temp`. If `None`, nothing
            will be plotted. Default is {}.

        Returns
        -------
        list of Line2D
            A list of lines representing the plotted data.
        """
        self._set_default_plot_params(
            min_temp_params, {"color": "#1f77b4", "label": "Minimum"}
        )
        self._set_default_plot_params(
            max_temp_params, {"color": "#d62728", "label": "Maximum"}
        )
        out = []
        components = [
            ("Min Temp", min_temp_params),
            ("Max Temp", max_temp_params),
        ]
        for column_name, param_dict in components:
            if param_dict is not None:
                (out_component,) = ax.plot(
                    mdates.date2num(self._x_dates),
                    self._lake_csv[column_name],
                    **param_dict,
                )
                out.append(out_component)
        ax.xaxis.set_major_formatter(self._date_formatter)
        ax.set_ylabel("Lake temperature (°C)")
        ax.set_xlabel("Date")
        return out


class NCProfile:
    """Profile timeseries plots for the `output.nc` file.

    Creates a profile plot of a variable for all depths and timesteps of 
    a GLM simulation. Reads the `output.nc` NetCDF file generated by GLM.

    Examples
    --------

    Plot the lake temperature and add a colour bar:
    >>> from glmpy import plots
    >>> import matplotlib.pyplot as plt
    >>> nc = plots.NCProfile("output.nc")
    >>> fig, ax = plt.subplots()
    >>> out = nc.plot_var(ax, "temp")
    >>> col_bar = fig.colorbar(out)
    >>> col_bar.set_label("Temperature (°C)")
    >>> plt.show()

    Plot the lake temperature with surface reference (instead of bottom 
    reference) and change the colour map:
    >>> nc = plots.NCProfile("plots_module_misc/example_outputs/output.nc")
    >>> fig, ax = plt.subplots()
    >>> out = nc.plot_var(ax, "temp", "surface", {"cmap": "viridis"})
    >>> col_bar = fig.colorbar(out)
    >>> col_bar.set_label("Temperature (°C)")
    >>> plt.show()

    Use `get_vars()` to return every valid variable name. Set the colour bar 
    label with `get_long_name()` (the unabbreviated variable name) and 
    `get_units()`:
    >>> var = nc.get_vars()[3]
    >>> long_name = nc.get_long_name(var)
    >>> units = nc.get_units(var)
    >>> fig, ax = plt.subplots()
    >>> out = nc.plot_var(ax, var)
    >>> col_bar = fig.colorbar(out)
    >>> col_bar.set_label(f"{long_name} ({units})")
    >>> plt.show()
    """
    def __init__(
            self, 
            glm_nc_path: str, 
            resolution: float=0.1,
            remove_ice: bool=False,
            remove_white_ice: bool=False,
            remove_snow: bool=False
        ):
        """Initialise the NCProfile with the `output.nc` NetCDF file.

        Parameters
        ----------
        glm_nc_path : str
            Path to the GLM `output.nc` NetCDF file.
        resolution : float
            Vertical resolution of plots in meters. Default is 0.1.
        remove_ice : bool
            Exclude black ice thickness from surface height. Default is False.
        remove_white_ice : bool
            Exclude white ice thickness from surface height. Default is False.  
        remove_snow : bool
            Exclude snow thickness from surface height. Default is False.
        """
        self._glm_nc = glm_nc_path
        self._resolution = resolution

        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        self._num_layers = nc.variables["NS"][:]
        self._layer_heights = nc.variables["z"][:]
        self._time = nc.variables["time"][:].data
        self._start_datetime = nc.start_time
        nc.close()

        self._surface_height = self._get_surface_height()
        if remove_ice or remove_white_ice or remove_snow:
            sum = self._sum_ice_snow(
                ice=remove_ice, white_ice=remove_white_ice, snow=remove_snow
            )
            self._surface_height = self._surface_height - sum
        self._max_depth = max(self._surface_height)
        self._depth_range = np.arange(0, self._max_depth, self._resolution)

    def _set_default_plot_params(
        self, param_dict: Union[dict, None], defaults_dict: dict
    ):
        if isinstance(param_dict, dict):
            for key, value in defaults_dict.items():
                if key not in param_dict:
                    param_dict[key] = value

    def _get_time(self):
        start_datetime = datetime.strptime(
            self._start_datetime, "%Y-%m-%d %H:%M:%S"
        )
        x_dates = [start_datetime + timedelta(hours=x) for x in self._time]
        x_dates = mdates.date2num(x_dates)

        return x_dates

    def _get_surface_height(self):
        """
        Returns a 1D array of the lake surface height at each timestep.
        """

        surface_height = ma.empty(self._num_layers.shape)
        for i in range(0, len(self._num_layers)):
            surface_height[i] = self._layer_heights[
                i, self._num_layers[i] - 1, 0, 0
            ]

        return surface_height
    
    def _sum_ice_snow(self, ice: bool, white_ice: bool, snow: bool):
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        time = nc.variables["time"][:].data
        sum = ma.zeros(shape=time.shape)
        if ice:
            ice_height = nc.variables["blue_ice_thickness"][:]
            sum += ice_height
        if white_ice:
            white_ice_height = nc.variables["white_ice_thickness"][:]
            sum += white_ice_height
        if snow:
            snow_height = nc.variables["snow_thickness"][:]
            sum += snow_height
        nc.close()
        return sum

    def _reproj_depth(
            self, layer_heights, var, plot_depths, reference, surface_height
        ):
        mid_layer_heights = ma.concatenate(
            [
                [layer_heights[0] / 2],
                layer_heights[0 : len(layer_heights) - 1]
                + (np.diff(layer_heights) / 2),
            ]
        )
        last_height = (
            ma.masked_all((1))
            if ma.is_masked(layer_heights[-1])
            else ma.array([layer_heights[-1]])
        )  
        last_var = (
            ma.masked_all((1))
            if ma.is_masked(var[-1])
            else ma.array([var[-1, 0, 0]])
        )  
        mid_layer_heights = ma.concatenate(
            [ma.array([0]), mid_layer_heights, last_height]
        )
        var = ma.concatenate([ma.array(var[0, 0]), var[:, 0, 0], last_var])
        valid_mask = ~ma.getmaskarray(mid_layer_heights) & ~ma.getmaskarray(
            var
        )
        mid_layer_heights = mid_layer_heights[valid_mask]
        var = var[valid_mask]
        reproj_var = np.interp(plot_depths, mid_layer_heights, var)
        if reference == "bottom":
            reproj_var[plot_depths > surface_height] = np.nan
        else:
            reproj_var[plot_depths < 0] = np.nan

        return reproj_var

    def _get_reproj_var(self, var, reference):
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        var = nc.variables[var][:]
        nc.close()

        max_num_layers = max(self._num_layers) + 1
        layer_heights = self._layer_heights[:, 0:max_num_layers, :, :]
        var = var[:, 0:max_num_layers, :, :]

        timesteps = layer_heights.shape[0]
        num_reproj_depths = len(self._depth_range)
        reproj_var = np.ma.empty((timesteps, num_reproj_depths))
        reproj_var[:] = np.nan

        if reference == "bottom":
            plot_depth_range = self._depth_range

        for i in range(0, timesteps):
            if reference == "surface":
                plot_depth_range = self._surface_height[i] - self._depth_range
            
            
            reproj_var[i, :] = self._reproj_depth(
                layer_heights=layer_heights[i, :, 0, 0],
                var=var[i, :],
                plot_depths=plot_depth_range,
                reference=reference,
                surface_height=self._surface_height[i]
            )
            
        if reference == "bottom":
            reproj_var = np.rot90(reproj_var, 1)
        else:
            reproj_var = np.rot90(reproj_var, -1)
            reproj_var = np.flip(reproj_var, 1)

        return reproj_var

    def _validate_data_range(self, data, min_diff=0.1):
        """Validate the data range and return suggested vmin/vmax if needed.
        
        Parameters
        ----------
        data : numpy.ma.core.MaskedArray
            The data array to validate
        min_diff : float
            Minimum required difference between min and max values
            
        Returns
        -------
        tuple
            (vmin, vmax) if range is too small, None otherwise
        """
        valid_data = data[~np.isnan(data)]
        if len(valid_data) == 0:
            return None
            
        data_min = np.min(valid_data)
        data_max = np.max(valid_data)
        data_range = data_max - data_min
        
        if data_range < min_diff:
            # If range is too small, create artificial range centered on mean
            mean_val = (data_max + data_min) / 2
            vmin = mean_val - min_diff/2
            vmax = mean_val + min_diff/2
            return (vmin, vmax)
        return None

    def plot_var(
        self,
        ax: Axes,
        var: str,
        reference: str = "bottom",
        param_dict: dict = {},
        min_diff: float = 0.1
    ) -> AxesImage:
        """Plot the profile timeseries of a variable on a matplotlib Axes.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Axes to plot on.
        var : str
            Name of the variable to plot. To list valid variables, see the 
            `get_vars()` method.
        reference : str, optional
            Reference frame for depth, either "bottom" or "surface". Default is 
            "bottom".
        param_dict : dict, optional
            Parameters passed to matplotlib.axes.Axes.imshow. Default is {}.
        min_diff : float, optional
            Minimum required difference between min and max values. If the actual
            range is smaller, artificial limits will be set. Default is 0.1.

        Returns
        -------
        matplotlib.image.AxesImage
            The plotted image
        """
        reproj_var = self._get_reproj_var(
            var=var, reference=reference
        )
        x_dates = self._get_time()
        
        # Validate data range and set vmin/vmax if needed
        range_limits = self._validate_data_range(reproj_var, min_diff)
        if range_limits is not None:
            param_dict['vmin'] = range_limits[0]
            param_dict['vmax'] = range_limits[1]

        # Calculate proper x-axis extent
        x_extent = [
            x_dates[0] - (x_dates[1] - x_dates[0])/2,  # Start half an interval before first date
            x_dates[-1] + (x_dates[1] - x_dates[0])/2  # End half an interval after last date
        ]

        self._set_default_plot_params(
            param_dict,
            {
                "interpolation": "bilinear",
                "aspect": "auto",
                "cmap": "Spectral_r",
                "extent": [x_extent[0], x_extent[1], self._max_depth, 0],
            },
        )

        out = ax.imshow(reproj_var, **param_dict)
        
        # Set x-axis ticks to actual dates
        ax.set_xticks(x_dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
        ax.set_ylabel("Depth (m)")
        ax.set_xlabel("Date")

        return out

    def get_vars(self) -> List[str]:
        """Get all available variables that can be plotted with `plot_var()`.

        Returns
        -------
        list of str
            Names of plottable variables in the NetCDF file
        """
        var_shape = self._layer_heights.shape
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        vars = []
        for key, value in nc.variables.items():
            if nc.variables[key].shape == var_shape:
                vars.append(key)
        nc.close()
        return vars

    def get_units(self, var: str) -> str:
        """Get the units of a variable.

        Parameters
        ----------
        var : str
            Name of the variable.

        Returns
        -------
        str
            Units of the variable.
        """
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        units = nc.variables[var].units
        nc.close()
        return units

    def get_long_name(self, var: str) -> str:
        """Get the long name description of a variable.

        Parameters
        ----------
        var : str
            Name of the variable.

        Returns
        -------
        str
            Long name description of the variable.
        """
        nc = netCDF4.Dataset(self._glm_nc, "r", format="NETCDF4")
        long_name = nc.variables[var].long_name
        nc.close()
        return long_name

    def get_start_datetime(self) -> datetime:
        """Get the simulation start time.

        Returns
        -------
        datetime.datetime
            Start time of the GLM simulation.
        """
        return datetime.strptime(self._start_datetime, "%Y-%m-%d %H:%M:%S")
