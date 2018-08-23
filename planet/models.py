import uuid
import pandas as pd
import urllib.parse as urlparse
import math
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from star.models import Star
from observatory.models import Observatory


DATA_SOURCE_TABLE_NAME = 'planets'
RA_RE = re.compile('(\d{2})h(\d{2})m(\d{2}\.\d{2})s')
DEC_RE = re.compile('(\+|-)(\d{2})d(\d{2})m(\d{2}\.\d{1})s')


class PlanetManager(models.Manager):

    def fetch_data(self):
        params = settings.DATA_SOURCE_PARAMS
        params['table'] = DATA_SOURCE_TABLE_NAME
        # print(params)
        url = '%s?%s' % (settings.DATA_SOURCE_URL, urlparse.urlencode(params))
        df = pd.read_csv(url)
        print(df.head())
        with pd.option_context('display.max_rows', None, 'display.max_columns', 999):
            for index, row in df.iterrows():

                print('##############################')
                print(row.to_frame().T)

                # start with parent/host star
                if pd.notna(row.pl_hostname):
                    try:
                        star = Star.objects.get(
                            name=row.pl_hostname
                        )
                    except Star.DoesNotExist:
                        star = Star(
                            name=row.pl_hostname,

                            ra_str=row.ra_str if pd.notna(row.ra_str) else None,
                            ra_str_err=row.st_raerr if pd.notna(row.st_raerr) else None,
                            ra=row.ra if pd.notna(row.ra) else None,

                            dec_str=row.dec_str if pd.notna(row.dec_str) else None,
                            dec_str_err=row.st_decerr if pd.notna(row.st_decerr) else None,
                            dec=row.dec if pd.notna(row.dec) else None,

                            distance=row.st_dist if pd.notna(row.st_dist) else None,
                            distance_err_up=row.st_disterr1 if pd.notna(row.st_disterr1) else None,
                            distance_err_low=row.st_disterr2 if pd.notna(row.st_disterr2) else None,
                            distance_limit=row.st_distlim if pd.notna(row.st_distlim) else None,
                            distance_nb_measures=row.st_distn if pd.notna(row.st_distn) else None,

                            magnitude_optical=row.st_optmag if pd.notna(row.st_optmag) else None,
                            magnitude_optical_err=row.st_optmagerr if pd.notna(row.st_optmagerr) else None,
                            magnitude_optical_limit=row.st_optmaglim if pd.notna(row.st_optmaglim) else None,
                            magnitude_gaia=row.gaia_gmag if pd.notna(row.gaia_gmag) else None,
                            magnitude_gaia_err=row.gaia_gmagerr if pd.notna(row.gaia_gmagerr) else None,
                            magnitude_gaia_limit=row.gaia_gmaglim if pd.notna(row.gaia_gmaglim) else None,

                            temperature=row.st_teff if pd.notna(row.st_teff) else None,
                            temperature_err_up=row.st_tefferr1 if pd.notna(row.st_tefferr1) else None,
                            temperature_err_low=row.st_tefferr2 if pd.notna(row.st_tefferr2) else None,
                            temperature_limit=row.st_tefflim if pd.notna(row.st_tefflim) else None,
                            temperature_nb_measures=row.st_teffn if pd.notna(row.st_teffn) else None,
                            mass=row.st_mass if pd.notna(row.st_mass) else None,

                            mass_err_up=row.st_masserr1 if pd.notna(row.st_masserr1) else None,
                            mass_err_low=row.st_masserr2 if pd.notna(row.st_masserr2) else None,
                            mass_limit=row.st_masslim if pd.notna(row.st_masslim) else None,
                            mass_nb_measures=row.st_massn if pd.notna(row.st_massn) else None,

                            radius=row.pl_radj if pd.notna(row.pl_radj) else None,
                            radius_err_up=row.pl_radjerr1 if pd.notna(row.pl_radjerr1) else None,
                            radius_err_low=row.pl_radjerr2 if pd.notna(row.pl_radjerr2) else None,
                            radius_limit=row.pl_radjlim if pd.notna(row.pl_radjlim) else None,
                            radius_nb_measures=row.pl_radn if pd.notna(row.pl_radn) else None,
                        )
                        # magnitude optical band
                        if pd.notna(row.st_optband):
                            if row.st_optband == 'V (Johnson)':
                                star.magnitude_optical_band = 1
                            elif row.st_optband == 'Kepler-band':
                                star.magnitude_optical_band = 2

                        star.save()

                # then observatory
                if pd.notna(row.pl_facility):
                    try:
                        observatory = Observatory.objects.get(
                            name=row.pl_facility
                        )
                    except Observatory.DoesNotExist:
                        observatory = Observatory(
                            name=row.pl_facility
                        )
                    observatory.save()

                # does the planet exist?
                try:
                    self.get(
                        name=row.pl_name
                    )
                except Planet.DoesNotExist:
                    planet = Planet(
                        star=star,
                        discovery_observatory=observatory,

                        letter=row.pl_letter if pd.notna(row.pl_letter) else None,
                        name=row.pl_name if pd.notna(row.pl_name) else None,

                        orbital_period=row.pl_orbper if pd.notna(row.pl_orbper) else None,
                        orbital_period_err_up=row.pl_orbpererr1 if pd.notna(row.pl_orbpererr1) else None,
                        orbital_period_err_low=row.pl_orbpererr2 if pd.notna(row.pl_orbpererr2) else None,
                        orbital_period_limit=row.pl_orbperlim if pd.notna(row.pl_orbperlim) else None,
                        orbital_period_nb_measures=row.pl_orbpern if pd.notna(row.pl_orbpern) else None,

                        orbit_semi_major_axis=row.pl_orbsmax if pd.notna(row.pl_orbsmax) else None,
                        orbit_semi_major_axis_err_up=row.pl_orbsmaxerr1 if pd.notna(row.pl_orbsmaxerr1) else None,
                        orbit_semi_major_axis_err_low=row.pl_orbsmaxerr2 if pd.notna(row.pl_orbsmaxerr2) else None,
                        orbit_semi_major_axis_limit=row.pl_orbsmaxlim if pd.notna(row.pl_orbsmaxlim) else None,
                        orbit_semi_major_axis_nb_measures=row.pl_orbsmaxn if pd.notna(row.pl_orbsmaxn) else None,

                        eccentricity=row.pl_orbeccen if pd.notna(row.pl_orbeccen) else None,
                        eccentricity_err_up=row.pl_orbeccenerr1 if pd.notna(row.pl_orbeccenerr1) else None,
                        eccentricity_err_low=row.pl_orbeccenerr2 if pd.notna(row.pl_orbeccenerr2) else None,
                        eccentricity_limit=row.pl_orbeccenlim if pd.notna(row.pl_orbeccenlim) else None,
                        eccentricity_nb_measures=row.pl_orbeccenn if pd.notna(row.pl_orbeccenn) else None,

                        orbit_inclination=row.pl_orbincl if pd.notna(row.pl_orbincl) else None,
                        orbit_inclination_err_up=row.pl_orbinclerr1 if pd.notna(row.pl_orbinclerr1) else None,
                        orbit_inclination_err_low=row.pl_orbinclerr2 if pd.notna(row.pl_orbinclerr2) else None,
                        orbit_inclination_limit=row.pl_orbincllim if pd.notna(row.pl_orbincllim) else None,
                        orbit_inclination_nb_measures=row.pl_orbincln if pd.notna(row.pl_orbincln) else None,

                        mass=row.pl_bmassj if pd.notna(row.pl_bmassj) else None,
                        mass_err_up=row.pl_bmassjerr1 if pd.notna(row.pl_bmassjerr1) else None,
                        mass_err_low=row.pl_bmassjerr2 if pd.notna(row.pl_bmassjerr2) else None,
                        mass_limit=row.pl_bmassjlim if pd.notna(row.pl_bmassjlim) else None,
                        mass_nb_measures=row.pl_bmassn if pd.notna(row.pl_bmassn) else None,

                        radius=row.pl_radj if pd.notna(row.pl_radj) else None,
                        radius_err_up=row.pl_radjerr1 if pd.notna(row.pl_radjerr1) else None,
                        radius_err_low=row.pl_radjerr2 if pd.notna(row.pl_radjerr2) else None,
                        radius_limit=row.pl_radjlim if pd.notna(row.pl_radjlim) else None,
                        radius_nb_measures=row.pl_radn if pd.notna(row.pl_radn) else None,

                        density=row.pl_dens if pd.notna(row.pl_dens) else None,
                        density_err_up=row.pl_denserr1 if pd.notna(row.pl_denserr1) else None,
                        density_err_low=row.pl_denserr2 if pd.notna(row.pl_denserr2) else None,
                        density_limit=row.pl_denslim if pd.notna(row.pl_denslim) else None,
                        density_nb_measures=row.pl_densn if pd.notna(row.pl_densn) else None,

                        is_ttv=True if row.pl_ttvflag == 1 else False,
                        is_kepler=True if row.pl_kepflag == 1 else False,
                        is_k2=True if row.pl_k2flag == 1 else False,

                        modified_official=row.rowupdate if pd.notna(row.rowupdate) else None,
                    )

                    # mass measurement type
                    if pd.notna(row.pl_bmassprov):
                        if pd.notna(row.pl_bmassprov) == 'Mass':
                            planet.mass_calculation_type = 1
                        elif pd.notna(row.pl_bmassprov) == 'Msin(i)/sin(i)':
                            planet.mass_calculation_type = 2
                        elif pd.notna(row.pl_bmassprov) == 'Msini':
                            planet.mass_calculation_type = 3

                    # discovery method
                    if pd.notna(row.pl_discmethod):
                        if row.pl_discmethod == 'Astrometry':
                            planet.discovery_method = 1
                        elif row.pl_discmethod == 'Eclipse Timing Variations':
                            planet.discovery_method = 2
                        elif row.pl_discmethod == 'Imaging':
                            planet.discovery_method = 3
                        elif row.pl_discmethod == 'Microlensing':
                            planet.discovery_method = 4
                        elif row.pl_discmethod == 'Orbital Brightness Modulation':
                            planet.discovery_method = 5
                        elif row.pl_discmethod == 'Pulsar Timing':
                            planet.discovery_method = 6
                        elif row.pl_discmethod == 'Pulsation Timing Variations':
                            planet.discovery_method = 7
                        elif row.pl_discmethod == 'Radial Velocity':
                            planet.discovery_method = 8
                        elif row.pl_discmethod == 'Transit':
                            planet.discovery_method = 9

                    # print(planet.__dict__)
                    planet.save()


class Planet(models.Model):
    """
    Model for planets
    native fields are taken "as is" from the data source but renamed
    st_ fields are shifted to a parent star object when needed
    """

    DISCOVERY_METHODS = (
        (1, _('Astrometry')),
        (2, _('Eclipse Timing Variations')),
        (3, _('Imaging')),
        (4, _('Microlensing')),
        (5, _('Orbital Brightness Modulation')),
        (6, _('Pulsar Timing')),
        (7, _('Pulsation Timing Variations')),
        (8, _('Radial Velocity')),
        (9, _('Transit')),
    )
    MASS_CALCULATION_TYPES = (
        (1, _('Mass')),
        (2, _('M*sin(i)/sin(i)')),
        (3, _('M*sin(i)')),
    )

    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, db_index=True)
    created = models.DateTimeField('Created', auto_now_add=True)
    modified_local = models.DateTimeField('Modified - local', auto_now=True)
    modified_official = models.DateField(_('Modified - official'), blank=False, null=False, help_text=_('[rowupdate] '
        'The date at which the planet was last officially updated'))

    star = models.ForeignKey(Star, null=False, blank=False, on_delete=models.PROTECT)

    letter = models.CharField(_('Letter'), max_length=2, blank=False, null=False, default=None,
        help_text=_('[pl_letter] Letter assigned to the planetary component of a planetary system'))
    name = models.CharField(_('Name'), max_length=120, blank=False, null=False, default=None,
        help_text=_('[pl_name] Planet name most commonly used in the literature'))
    discovery_method = models.PositiveSmallIntegerField(_('Discovery method'), choices=DISCOVERY_METHODS, blank=False,
        null=False, default=9, help_text=_('[pl_discmethod] Method by which the planet was first identified'))
    discovery_observatory = models.ForeignKey(Observatory, null=True, blank=True, on_delete=models.PROTECT,
        help_text=_('[pl_facility]'))

    # orbital period
    orbital_period = models.DecimalField(_('Orbital period (days)'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbper] Time the planet takes to make a complete orbit around '
                                                    'the host star or system'))
    orbital_period_err_up = models.DecimalField(_('Orbital period upper error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbpererr1]'))
    orbital_period_err_low = models.DecimalField(_('Orbital period lower error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbpererr2]'))
    orbital_period_limit = models.DecimalField(_('Orbital period limit'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbperlim]'))
    orbital_period_nb_measures = models.PositiveSmallIntegerField(_('Orbital period number of measures'), blank=False,
        null=False, default=0, help_text=_('[pl_orbpern]'))

    # orbit semi-major axis
    orbit_semi_major_axis = models.DecimalField(_('Orbit Semi-Major Axis (AU)'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbsmax] The longest radius of an elliptic orbit, or, for '
                                                    'exoplanets detected via gravitational microlensing or direct imaging, '
                                                    'the projected separation in the plane of the sky'))
    orbit_semi_major_axis_err_up = models.DecimalField(_('Orbit Semi-Major Axis upper error margin'),
        max_digits=20, decimal_places=10, blank=True, null=True, help_text=_('[pl_orbsmaxerr1]'))
    orbit_semi_major_axis_err_low = models.DecimalField(_('Orbit Semi-Major Axis lower error margin'),
        max_digits=20, decimal_places=10, blank=True, null=True, help_text=_('[pl_orbsmaxerr2]'))
    orbit_semi_major_axis_limit = models.DecimalField(_('Orbit Semi-Major Axis limit'), blank=True, null=True,
                                                max_digits=20, decimal_places=10, help_text=_('[pl_orbsmaxlim]'))
    orbit_semi_major_axis_nb_measures = models.PositiveSmallIntegerField(_('Orbit Semi-Major Axis number of measures'),
        blank=False, null=False, default=0, help_text=_('[pl_orbsmaxn]'))

    # eccentricity
    eccentricity = models.DecimalField(_('Eccentricity'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbeccen] Amount by which the orbit of the planet deviates '
                                                    'from a perfect circle'))
    eccentricity_err_up = models.DecimalField(_('Eccentricity upper error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbeccenerr1]'))
    eccentricity_err_low = models.DecimalField(_('Eccentricity lower error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbeccenerr1]'))
    eccentricity_limit = models.DecimalField(_('Eccentricity limit'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbeccenlim]'))
    eccentricity_nb_measures = models.PositiveSmallIntegerField(_('Orbit Semi-Major Axis number of measures'),
        blank=False, null=False, default=0, help_text=_('[pl_orbeccenn]'))

    # orbit inclination
    orbit_inclination = models.DecimalField(_('Orbit inclination (deg)'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbincl] Angular distance of the orbital plane from '
                                                    'the line of sight'))
    orbit_inclination_err_up = models.DecimalField(_('Orbit inclination upper error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_orbinclerr1]'))
    orbit_inclination_err_low = models.DecimalField(_('Orbit inclination lower error margin'), blank=True, null=True,
       max_digits=20, decimal_places=10, help_text=_('[pl_orbinclerr2]'))
    orbit_inclination_limit = models.DecimalField(_('Orbit inclination limit'), blank=True, null=True,
       max_digits=20, decimal_places=10, help_text=_('[pl_orbincllim]'))
    orbit_inclination_nb_measures = models.PositiveSmallIntegerField(_('Orbit inclination number of measures'),
       blank=False, null=False, default=0, help_text=_('[pl_orbincln]'))

    # mass
    mass = models.DecimalField(_('Mass (J)'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_bmassj] Best planet mass measurement in units of masses of Jupiter'))
    mass_err_up = models.DecimalField(_('Mass upper error margin'), blank=True, null=True, max_digits=20, 
        decimal_places=10, help_text=_('[pl_bmassjerr1]'))
    mass_err_low = models.DecimalField(_('Mass lower error margin'), blank=True, null=True, max_digits=20, 
        decimal_places=10, help_text=_('[pl_bmassjerr2]'))
    mass_limit = models.DecimalField(_('Mass limit'), blank=True, null=True, max_digits=20, decimal_places=10, 
        help_text=_('[pl_bmassjlim]'))
    mass_nb_measures = models.PositiveSmallIntegerField(_('Mass number of measures'),
        blank=False, null=False, default=0, help_text=_('[pl_bmassn]'))
    mass_calculation_type = models.PositiveSmallIntegerField(_('Mass calculation type'), choices=MASS_CALCULATION_TYPES,
        blank=False, null=False, default=0, help_text=_('[pl_bmassprov]'))

    # radius
    radius = models.DecimalField(_('Radius (Jupiter radii)'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_radj] Length of a line segment from the center of the planet '
                                                     'to its surface, measured in units of radius of Jupiter'))
    radius_err_up = models.DecimalField(_('Radius upper error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_radjerr1]'))
    radius_err_low = models.DecimalField(_('Radius lower error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_radjerr2]'))
    radius_limit = models.DecimalField(_('Radius limit'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_radjlim]'))
    radius_nb_measures = models.PositiveSmallIntegerField(_('Radius number of measures'),
        blank=False, null=False, default=0, help_text=_('[pl_radn]'))

    # density
    density = models.DecimalField(_('Density (g/cm-3)'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_dens] Amount of mass per unit of volume of the planet'))
    density_err_up = models.DecimalField(_('Density upper error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_denserr1]'))
    density_err_low = models.DecimalField(_('Density lower error margin'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_denserr2]'))
    density_limit = models.DecimalField(_('Density limit'), blank=True, null=True,
        max_digits=20, decimal_places=10, help_text=_('[pl_denslim]'))
    density_nb_measures = models.PositiveSmallIntegerField(_('Density number of measures'),
        blank=False, null=False, default=0, help_text=_('[pl_densn]'))

    is_ttv = models.BooleanField(_('Is TTV'), blank=False, default=False,
        help_text=_('[pl_ttvflag] Flag indicating if the planet orbit exhibits transit timing variations from '
                    'another planet in the system'))
    is_kepler = models.BooleanField(_('Is Kepler'), blank=False, default=False,
        help_text=_('[pl_kepflag] Flag indicating if the planetary system signature is present in data taken with the '
                    'Kepler mission'))
    is_k2 = models.BooleanField(_('Is K2'), blank=False, default=False,
        help_text=_('[pl_k2flag] Flag indicating if the planetary system signature is present in data taken with '
                    'the K2 Mission'))

    objects = PlanetManager()

    def __str__(self):
        return self.name