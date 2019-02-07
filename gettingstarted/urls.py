from django.conf.urls import include, url

from hello import views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.lineal, name='lineal'),
    url(r'^aditivo/$', views.aditivo, name='Aditivo'),
    url(r'^multiplica/$', views.multiplicativo, name='Multiplicativo'),
    url(r'^random/$', views.random, name='Random'),
    url(r'^postData/$', views.postData, name='postData'),
    #Iframes
    url(r'^metodoLineal$', views.metodoLineal, name='metodoLineal'),
    url(r'^metodoAditivo/$', views.metodoAditivo, name='metodoAditivo'),
    url(r'^metodoMultiplica/$', views.metodoMultiplicativo, name='metodoMultiplicativo'),
    url(r'^metodoRandom/$', views.metodoRandom, name='metodoRandom'),
    url(r'^metodoPostData/$', views.metodoPostData, name='metodoPostData'),
    #Url para metodos
    url(r'^promedioMovil/$', views.promedioMovil, name='promedioMovil'),
    url(r'^alisamiento/$', views.alisamiento, name='alisamiento'),
    url(r'^regreLineal/$', views.regreLineal, name='regreLineal'),
    url(r'^regreCuadrado/$', views.regreCuadrado, name='regreCuadrado'),
    #Simulaciones
    url(r'^montecarlo/$', views.montecarlo, name='montecarlo'),
    url(r'^lineaEspera/$', views.lineaEspera, name='lineaEspera'),
    url(r'^lineaEsperaMonte/$', views.lineaEsperaMonte, name='lineaEsperaMonte'),
    url(r'^inventarioMontecarlo/$', views.inventarioMontecarlo, name='inventarioMontecarlo'),
    url(r'^profile/$', views.profile, name='profile'),

]

