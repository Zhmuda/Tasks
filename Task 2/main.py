import csv
from django.db import models
from django.utils import timezone


class Player(models.Model):
    player_id = models.CharField(max_length=100)
    
    
class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    
class Prize(models.Model):
    title = models.CharField(max_length=100)
    
    
class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    
    def assign_prize(self):
        if self.is_completed:
            # Проверяем, есть ли приз для этого уровня
            level_prize = LevelPrize.objects.filter(level=self.level).first()
            if level_prize:
                # Присваиваем приз игроку
                level_prize.received = timezone.now()
                level_prize.save()
                return level_prize.prize
        return None
    
    
class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField(null=True, blank=True)
    
    
def export_player_levels_to_csv(file_path):
    player_levels = PlayerLevel.objects.select_related('player', 'level').iterator(chunk_size=1000)
    
    level_prize_dict = {lp.level_id: lp.prize.title for lp in LevelPrize.objects.all()}
    
    # Открываем файл для записи
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Player ID', 'Level Title', 'Is Completed', 'Prize Title'])
        
        for pl in player_levels:
            prize_title = level_prize_dict.get(pl.level_id, 'No Prize')
            writer.writerow([pl.player.player_id, pl.level.title, pl.is_completed, prize_title])
