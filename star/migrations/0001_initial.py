# Generated by Django 2.0.8 on 2018-08-23 20:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, verbose_name='UUID')),
                ('name', models.CharField(default=None, help_text='[pl_hostname] Stellar name most commonly used', max_length=120, verbose_name='Name')),
                ('ra_str', models.CharField(blank=True, help_text='[ra_str] Right Ascension in sexagesimal format.', max_length=20, null=True, verbose_name='Right ascension')),
                ('ra_str_err', models.DecimalField(blank=True, decimal_places=10, help_text='[st_raerr]', max_digits=20, null=True, verbose_name='Right ascension error margin')),
                ('ra', models.DecimalField(blank=True, decimal_places=10, help_text='[ra] in decimal degrees', max_digits=20, null=True, verbose_name='Right ascension')),
                ('dec_str', models.CharField(blank=True, help_text='[dec_str] Declination in sexagesimal format.', max_length=20, null=True, verbose_name='Declination')),
                ('dec_str_err', models.DecimalField(blank=True, decimal_places=10, help_text='[st_decerr]', max_digits=20, null=True, verbose_name='Declination error margin')),
                ('dec', models.DecimalField(blank=True, decimal_places=10, help_text='[dec] in decimal degrees', max_digits=20, null=True, verbose_name='Declination')),
                ('distance', models.DecimalField(blank=True, decimal_places=10, help_text='[st_dist] Distance to the planetary system in units of parsecs', max_digits=20, null=True, verbose_name='Distance')),
                ('distance_err_up', models.DecimalField(blank=True, decimal_places=10, help_text='[st_disterr1] in parsecs', max_digits=20, null=True, verbose_name='Distance upper error margin')),
                ('distance_err_low', models.DecimalField(blank=True, decimal_places=10, help_text='[st_disterr2] in parsecs', max_digits=20, null=True, verbose_name='Distance lower error margin')),
                ('distance_limit', models.DecimalField(blank=True, decimal_places=10, help_text='[st_distlim]', max_digits=20, null=True, verbose_name='Distance limit')),
                ('distance_nb_measures', models.PositiveSmallIntegerField(default=0, help_text='[st_distn]', verbose_name='Distance number of measures')),
                ('magnitude_optical', models.DecimalField(blank=True, decimal_places=10, help_text='[st_optmag] Brightness of the host star as measured using the V (Johnson) or the Kepler-band in units of magnitudes', max_digits=20, null=True, verbose_name='Optical magnitude (mag)')),
                ('magnitude_optical_err', models.DecimalField(blank=True, decimal_places=10, help_text='[st_optmagerr]', max_digits=20, null=True, verbose_name='Optical magnitude error margin')),
                ('magnitude_optical_limit', models.DecimalField(blank=True, decimal_places=10, help_text='[st_optmaglim]', max_digits=20, null=True, verbose_name='Optical magnitude limit')),
                ('magnitude_optical_band', models.PositiveSmallIntegerField(choices=[(1, 'V (Johnson)'), (2, 'Kepler-band')], default=1, help_text='[st_optband]', verbose_name='Optical magnitude band')),
                ('magnitude_gaia', models.DecimalField(blank=True, decimal_places=10, help_text='[gaia_gmag] Brightness of the host star as measuring using the Gaia band in units of magnitudes', max_digits=20, null=True, verbose_name='G-band (Gaia) (mag)')),
                ('magnitude_gaia_err', models.DecimalField(blank=True, decimal_places=10, help_text='[gaia_gmagerr]', max_digits=20, null=True, verbose_name='G-band (Gaia) error margin')),
                ('magnitude_gaia_limit', models.DecimalField(blank=True, decimal_places=10, help_text='[gaia_gmaglim]', max_digits=20, null=True, verbose_name='G-band (Gaia) limit')),
                ('temperature', models.DecimalField(blank=True, decimal_places=10, help_text='[st_teff] Temperature of the star as modeled by a black body emitting the same total amount of electromagnetic radiations', max_digits=20, null=True, verbose_name='Effective temperature (K)')),
                ('temperature_err_up', models.DecimalField(blank=True, decimal_places=10, help_text='[st_tefferr1] in parsecs', max_digits=20, null=True, verbose_name='Effective temperature upper error margin')),
                ('temperature_err_low', models.DecimalField(blank=True, decimal_places=10, help_text='[st_tefferr2] in parsecs', max_digits=20, null=True, verbose_name='Effective temperature lower error margin')),
                ('temperature_limit', models.DecimalField(blank=True, decimal_places=10, help_text='[st_tefflim]', max_digits=20, null=True, verbose_name='Effective temperature limit')),
                ('temperature_nb_measures', models.PositiveSmallIntegerField(default=0, help_text='[st_teffn]', verbose_name='Effective temperature number of measures')),
                ('mass', models.DecimalField(blank=True, decimal_places=10, help_text='[st_mass] Amount of matter contained in the star, measured in units of masses of the Sun', max_digits=20, null=True, verbose_name='Mass (solar mass)')),
                ('mass_err_up', models.DecimalField(blank=True, decimal_places=10, help_text='[st_masserr1] in parsecs', max_digits=20, null=True, verbose_name='Mass upper error margin')),
                ('mass_err_low', models.DecimalField(blank=True, decimal_places=10, help_text='[st_masserr2] in parsecs', max_digits=20, null=True, verbose_name='Mass lower error margin')),
                ('mass_limit', models.DecimalField(blank=True, decimal_places=10, help_text='[st_masslim]', max_digits=20, null=True, verbose_name='Mass limit')),
                ('mass_nb_measures', models.PositiveSmallIntegerField(default=0, help_text='[st_massn]', verbose_name='Mass number of measures')),
                ('radius', models.DecimalField(blank=True, decimal_places=10, help_text='[pl_radj] Amount of matter contained in the star, measured in units of masses of the Sun', max_digits=20, null=True, verbose_name='Radius (solar radii)')),
                ('radius_err_up', models.DecimalField(blank=True, decimal_places=10, help_text='[pl_radjerr1] in parsecs', max_digits=20, null=True, verbose_name='Radius upper error margin')),
                ('radius_err_low', models.DecimalField(blank=True, decimal_places=10, help_text='[pl_radjerr2] in parsecs', max_digits=20, null=True, verbose_name='Radius lower error margin')),
                ('radius_limit', models.DecimalField(blank=True, decimal_places=10, help_text='[pl_radjlim]', max_digits=20, null=True, verbose_name='Radius limit')),
                ('radius_nb_measures', models.PositiveSmallIntegerField(default=0, help_text='[pl_radn]', verbose_name='Radius number of measures')),
            ],
        ),
    ]
