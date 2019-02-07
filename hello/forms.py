from django import forms


class linealForm(forms.Form):
	M = forms.IntegerField(initial=131)
	Xn = forms.IntegerField(initial=77)
	A = forms.IntegerField(initial=31)
	C = forms.IntegerField(initial=31)
	N = forms.IntegerField(initial=20)

class adiForm(forms.Form):
	M = forms.IntegerField(initial=100)
	Xo = forms.IntegerField(initial=77)
	Xn = forms.IntegerField(initial=1)
	N = forms.IntegerField(initial=20)

class multiForm(forms.Form):
	M = forms.IntegerField(initial=1000)
	Xn = forms.IntegerField(initial=31)
	A = forms.IntegerField(initial=77)
	C = forms.IntegerField(initial=7)
	N = forms.IntegerField(initial=20)

class randomForm(forms.Form):
	N = forms.IntegerField(initial=20)

class pruebaForm(forms.Form):
	N = forms.CharField()

class sideseo(forms.Form):
	CHOICES = (('1', 'Nuevo Calculo',), ('2', 'Seleccionar Numeros ',))
	Escoja = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

#formulario para generar mas campos
class generaForm(forms.Form):
	N = forms.IntegerField(initial=5)

	