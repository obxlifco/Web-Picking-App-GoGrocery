import { NgModule } from '@angular/core';
import {FormsModule} from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HomeRoutingModule } from './home-routing.module';
import { HomeComponent } from './app.home.component';
import {PipeModule} from '../../global/pipes/pipe.module';
import {CmsModule} from '../cms/cms.module';
import {MaterialModule} from '../../global/modules/material.module';
@NgModule({
  declarations: [HomeComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    PipeModule,
    CmsModule,
    MaterialModule,
    FormsModule,
  ]
})
export class HomeModule { }
