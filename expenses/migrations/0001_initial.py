import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Tên danh mục')),
                ('kind', models.CharField(choices=[('income', 'Thu'), ('expense', 'Chi')], max_length=10, verbose_name='Loại')),
                ('color', models.CharField(default='#3D7A5A', max_length=7, verbose_name='Màu')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Danh mục',
                'verbose_name_plural': 'Danh mục',
                'ordering': ['kind', 'name'],
            },
        ),
        migrations.CreateModel(
            name='MonthlyBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(verbose_name='Năm')),
                ('month', models.PositiveSmallIntegerField(verbose_name='Tháng')),
                ('limit', models.DecimalField(decimal_places=0, max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('1'))], verbose_name='Hạn mức (VNĐ)')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='expenses.category', verbose_name='Danh mục chi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ngân sách tháng',
                'verbose_name_plural': 'Ngân sách tháng',
                'ordering': ['-year', '-month', 'category__name'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('1'))], verbose_name='Số tiền (VNĐ)')),
                ('occurred_on', models.DateField(default=django.utils.timezone.localdate, verbose_name='Ngày')),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='Ghi chú')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='expenses.category', verbose_name='Danh mục')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Giao dịch',
                'verbose_name_plural': 'Giao dịch',
                'ordering': ['-occurred_on', '-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('user', 'name', 'kind'), name='uniq_category_per_user_kind'),
        ),
        migrations.AddConstraint(
            model_name='monthlybudget',
            constraint=models.UniqueConstraint(fields=('user', 'category', 'year', 'month'), name='uniq_budget_per_category_month'),
        ),
        migrations.AddConstraint(
            model_name='monthlybudget',
            constraint=models.CheckConstraint(condition=models.Q(('month__gte', 1), ('month__lte', 12)), name='budget_month_1_12'),
        ),
    ]
