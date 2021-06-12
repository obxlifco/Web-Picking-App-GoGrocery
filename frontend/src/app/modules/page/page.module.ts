import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule} from '@angular/forms';
import { PageRoutingModule } from './page-routing.module';
import {PageComponent} from './app.page.component';
import {PipeModule} from '../../global/pipes/pipe.module';
import {MaterialModule} from '../../global/modules/material.module';
import {CmsModule} from '../cms/cms.module'

@NgModule({
  declarations: [
                 PageComponent,
                ],
  imports: [
    CommonModule,
    PageRoutingModule,
    PipeModule,
    MaterialModule,
    FormsModule,
    CmsModule
   
  ]
})
export class PageModule { }
