import { NgModule } from '@angular/core';
import { ServerModule, ServerTransferStateModule } from '@angular/platform-server';
import { AppModule } from './app.module';
import { AppComponent } from './app.component';
import { ModuleMapLoaderModule } from '@nguniversal/module-map-ngfactory-loader';
import { NgtPwaMockModule } from '@ng-toolkit/pwa';
import { ServerCookiesModule } from '@ngx-utils/cookies/server';
import { CookieService, CookieBackendService } from 'ngx-cookie';

/*import { AgmCoreModule } from '@agm/core';*/

@NgModule({
  imports: [
    AppModule,
    ServerModule,
    ModuleMapLoaderModule,
    ServerTransferStateModule,
    NgtPwaMockModule,
    /*AgmCoreModule.forRoot({
      apiKey: 'AIzaSyDwJfFz9Hyur4RkbEa_Hlt6Fkibr6rYhJo',
      libraries: ['places','geocode','maps']
    }),*/
    ServerCookiesModule.forRoot(),
  ],
  bootstrap: [AppComponent],
  providers: [{ provide: CookieService, useClass: CookieBackendService }],
})
export class AppServerModule {}
