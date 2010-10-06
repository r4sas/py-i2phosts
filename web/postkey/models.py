from django.db import models

class i2phost(models.Model):
	# Hostname limit is 67 characters maximum, including the '.i2p'.
	name = models.CharField("I2P hostname", max_length=67)
	# Maximum key length 616 bytes (to account for certs up to 100 bytes).
	b64hash = models.CharField("b64 hash", max_length=616)
	date_added = models.DateTimeField(auto_now_add=True)
	activated = models.BooleanField(default=False)