import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Count, Q, Sum, Avg, F
from main_app.models import Astronaut, Mission, Spacecraft


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts.exists():
        return ""

    result = []
    for astronaut in astronauts:
        status = 'Active' if astronaut.is_active else 'Inactive'
        result.append(f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {status}")

    return "\n".join(result)


def get_top_astronaut():
    astronaut = Astronaut.objects.annotate(
        missions_count=Count('missions')
    ).order_by('-missions_count', 'phone_number').first()

    if not astronaut or astronaut.missions_count == 0:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions."


def get_top_commander():
    astronaut = Astronaut.objects.annotate(
        commanded_missions_count=Count('commanded_missions')
    ).order_by('-commanded_missions_count', 'phone_number').first()

    if not astronaut or astronaut.commanded_missions_count == 0:
        return "No data."

    return f"Top Commander: {astronaut.name} with {astronaut.commanded_missions_count} commanded missions."


def get_last_completed_mission():
    last_completed_mission = Mission.objects.filter(status=Mission.COMPLETED).order_by('-launch_date').first()

    if not last_completed_mission:
        return "No data."

    commander_name = last_completed_mission.commander.name if last_completed_mission.commander else "TBA"

    astronaut_names = (last_completed_mission.astronauts
                       .order_by('name')
                       .values_list('name', flat=True))

    total_spacewalks = last_completed_mission.astronauts.aggregate(Sum('spacewalks'))['spacewalks__sum'] or 0

    return (f"The last completed mission is: {last_completed_mission.name}. "
            f"Commander: {commander_name}. "
            f"Astronauts: {', '.join(astronaut_names)}. "
            f"Spacecraft: {last_completed_mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    if not Mission.objects.exists():
        return "No data."

    most_used_spacecraft = (Spacecraft.objects
                            .annotate(num_missions=Count('mission'))
                            .order_by('-num_missions', 'name')
                            .first())

    if not most_used_spacecraft:
        return "No data."

    num_astronauts = (Mission.objects
                      .filter(spacecraft=most_used_spacecraft)
                      .values_list('astronauts', flat=True)
                      .distinct()
                      .count())

    num_missions = most_used_spacecraft.num_missions

    return (f"The most used spacecraft is: {most_used_spacecraft.name}, "
            f"manufactured by {most_used_spacecraft.manufacturer}, "
            f"used in {num_missions} missions, "
            f"astronauts on missions: {num_astronauts}.")


def decrease_spacecrafts_weight():
    planned_mission_spacecrafts = Spacecraft.objects.filter(
        mission__status='Planned',
        weight__gte=200.0
    ).distinct()

    affected_spacecrafts_count = planned_mission_spacecrafts.update(weight=F('weight') - 200.0)

    if affected_spacecrafts_count == 0:
        return "No changes in weight."

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']
    avg_weight = avg_weight if avg_weight is not None else 0.0

    return (f"The weight of {affected_spacecrafts_count} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg.")
