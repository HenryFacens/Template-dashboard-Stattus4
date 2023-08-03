# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clients(models.Model):
    id = models.UUIDField(primary_key=True)
    trading_name = models.CharField()
    corporate_name = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = models.BooleanField()
    client_id_master = models.UUIDField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)
    number = models.CharField(blank=True, null=True)
    complement = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    state = models.CharField(blank=True, null=True)
    zip_code = models.CharField(blank=True, null=True)
    comments = models.CharField(blank=True, null=True)
    contact = models.CharField(blank=True, null=True)
    telephone = models.CharField(blank=True, null=True)
    lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    long = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cnpj = models.CharField(blank=True, null=True)
    neighborhood = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class ConnectivityData(models.Model):
    install_point_id = models.BigIntegerField(primary_key=True)  # The composite primary key (install_point_id, device_id, timestamp) found, that is not supported. The first column is selected.
    device_id = models.CharField()
    timestamp = models.DateTimeField()
    meter_id = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    info_type = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    info = models.TextField(blank=True, null=True)  # This field type is a guess.
    client_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'connectivity_data'
        unique_together = (('install_point_id', 'device_id', 'timestamp'),)


class ConnectivityRate(models.Model):
    install_point_id = models.BigIntegerField(primary_key=True)  # The composite primary key (install_point_id, device_id, timestamp) found, that is not supported. The first column is selected.
    device_id = models.CharField()
    meter_id = models.CharField(blank=True, null=True)
    conn_rate = models.FloatField(blank=True, null=True)
    conn_evt = models.SmallIntegerField(blank=True, null=True)
    communication_day = models.SmallIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tx = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'connectivity_rate'
        unique_together = (('install_point_id', 'device_id', 'timestamp'),)


class DeviceSchema(models.Model):
    version = models.CharField(primary_key=True)
    type = models.CharField(blank=True, null=True)
    brand = models.CharField(blank=True, null=True)
    client_id = models.UUIDField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    setup = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'device_schema'


class DeviceSchemaCategoriesMetadataDevice(models.Model):
    deviceschemaversion = models.OneToOneField(DeviceSchema, models.DO_NOTHING, db_column='deviceSchemaVersion', primary_key=True)  # Field name made lowercase. The composite primary key (deviceSchemaVersion, metadataDeviceId, metadataDeviceNameId, metadataDeviceInfoType) found, that is not supported. The first column is selected.
    metadatadeviceid = models.ForeignKey('MetadataDevice', models.DO_NOTHING, db_column='metadataDeviceId')  # Field name made lowercase.
    metadatadevicenameid = models.CharField(db_column='metadataDeviceNameId')  # Field name made lowercase.
    metadatadeviceinfotype = models.CharField(db_column='metadataDeviceInfoType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'device_schema_categories_metadata_device'
        unique_together = (('deviceschemaversion', 'metadatadeviceid', 'metadatadevicenameid', 'metadatadeviceinfotype'),)


class DeviceState(models.Model):
    install_point_id = models.BigIntegerField(primary_key=True)  # The composite primary key (install_point_id, device_id, metadata_device_id) found, that is not supported. The first column is selected.
    device_id = models.CharField()
    metadata_device_id = models.BigIntegerField()
    meter_id = models.CharField(blank=True, null=True)
    info_type = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)  # This field type is a guess.
    client_id = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'device_state'
        unique_together = (('install_point_id', 'device_id', 'metadata_device_id'),)


class Devices(models.Model):
    id = models.CharField(primary_key=True)
    install_point_id = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)
    version = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    setup = models.TextField(blank=True, null=True)  # This field type is a guess.
    serial_number = models.CharField(blank=True, null=True)
    client_id = models.UUIDField(blank=True, null=True)
    communication = models.TextField(blank=True, null=True)  # This field type is a guess.
    driver = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devices'


class DevicesData(models.Model):
    install_point_id = models.BigIntegerField(primary_key=True)  # The composite primary key (install_point_id, device_id, timestamp) found, that is not supported. The first column is selected.
    device_id = models.CharField()
    timestamp = models.DateTimeField()
    meter_id = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    single_value = models.FloatField(blank=True, null=True)
    composed_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client_id = models.UUIDField(blank=True, null=True)
    alarm = models.BooleanField(blank=True, null=True)
    metadata_device_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devices_data'
        unique_together = (('install_point_id', 'device_id', 'timestamp'),)


class EventData(models.Model):
    install_point_id = models.BigIntegerField(primary_key=True)  # The composite primary key (install_point_id, device_id, timestamp, metadata_device_id) found, that is not supported. The first column is selected.
    device_id = models.CharField()
    timestamp = models.DateTimeField()
    meter_id = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client_id = models.UUIDField(blank=True, null=True)
    metadata_device_id = models.BigIntegerField()
    info = models.TextField(blank=True, null=True)  # This field type is a guess.
    info_type = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_data'
        unique_together = (('install_point_id', 'device_id', 'timestamp', 'metadata_device_id'),)


class InstallPoints(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    alt = models.FloatField(blank=True, null=True)
    precision = models.FloatField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)
    number = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    state = models.CharField(blank=True, null=True)
    country = models.CharField(blank=True, null=True)
    zipcode = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    user_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    timezone = models.IntegerField()
    setup = models.TextField(blank=True, null=True)  # This field type is a guess.
    client_id = models.UUIDField(blank=True, null=True)
    neighborhood = models.CharField(blank=True, null=True)
    complement = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'install_points'


class Issues(models.Model):
    id = models.UUIDField(primary_key=True)
    slug = models.CharField()
    subject = models.TextField(blank=True, null=True)  # This field type is a guess.
    level = models.CharField()
    solved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'issues'


class MetadataDevice(models.Model):
    id = models.BigAutoField(primary_key=True)  # The composite primary key (id, name_id, info_type) found, that is not supported. The first column is selected.
    name_id = models.CharField()
    info_type = models.CharField()
    name = models.TextField()  # This field type is a guess.
    type = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    client_id = models.UUIDField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'metadata_device'
        unique_together = (('id', 'name_id', 'info_type'),)


class MeterDeviceInstallPoint(models.Model):
    install_point_id = models.BigIntegerField(primary_key=True)  # The composite primary key (install_point_id, device_id) found, that is not supported. The first column is selected.
    device_id = models.CharField()
    meter_id = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField()
    active = models.BooleanField()
    end_time = models.DateTimeField(blank=True, null=True)
    setup = models.TextField(blank=True, null=True)  # This field type is a guess.
    updated_at = models.DateTimeField()
    alarm_boundaries = models.TextField(blank=True, null=True)  # This field type is a guess.
    alarms = models.TextField(blank=True, null=True)  # This field type is a guess.
    set_image = models.TextField(blank=True, null=True)
    device_image = models.TextField(blank=True, null=True)
    week_communication = models.BigIntegerField(blank=True, null=True)
    last_communication = models.TextField(blank=True, null=True)
    programmed_communication_day = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meter_device_install_point'
        unique_together = (('install_point_id', 'device_id'),)


class Meters(models.Model):
    id = models.CharField(primary_key=True)
    type = models.CharField(blank=True, null=True)
    brand = models.CharField(blank=True, null=True)
    tags = models.CharField(blank=True, null=True)
    setup = models.TextField(blank=True, null=True)  # This field type is a guess.
    user_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meters'


class RouteMap(models.Model):
    path = models.CharField()
    method = models.CharField()
    namespace = models.CharField()
    hits = models.BigIntegerField()
    last_access = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'route_map'


class Tags(models.Model):
    client_id = models.UUIDField(primary_key=True)  # The composite primary key (client_id, id_name) found, that is not supported. The first column is selected.
    id_name = models.CharField()
    name = models.CharField(blank=True, null=True)
    color = models.CharField(blank=True, null=True)
    tag_master = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'
        unique_together = (('client_id', 'id_name'),)


class Tokens(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'


class TypeormMetadata(models.Model):
    type = models.CharField()
    database = models.CharField(blank=True, null=True)
    schema = models.CharField(blank=True, null=True)
    table = models.CharField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typeorm_metadata'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    pwd_hash = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    client_id = models.UUIDField(blank=True, null=True)
    type_user = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField()
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users_roles'
