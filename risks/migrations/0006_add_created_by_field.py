from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # This may be different in your project
        ('risks', '0005_remove_old_category'),  # Update with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='risk',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='risks',
                to='auth.user',
            ),
        ),
    ]