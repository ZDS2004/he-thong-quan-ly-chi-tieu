import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='note_date',
            field=models.DateField(default=django.utils.timezone.localdate, verbose_name='Ngày ghi chú'),
        ),
    ]
