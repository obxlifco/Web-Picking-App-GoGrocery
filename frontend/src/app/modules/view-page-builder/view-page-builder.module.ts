import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule} from '@angular/forms';
import {ViewPageBuilderComponent} from './view-page-builder.component';
import {EditWidgetComponent,FormAddEditFieldComponent} from './edit-widget/edit-widget.component';
import {MaterialModule} from '../../global/modules/material.module';
import {SharedModule} from '../../global/modules/shared.module';
import {PipeModule} from '../../global/pipes/pipe.module';
import {AddEditPageComponent,ManagePageComponent,AddEditNavigationComponent,ManageNavigationComponent,} from './page-setup/page.setup.component';
import { ViewPageBuilderRoutingModule } from './view-page-builder-routing.module';
import {DragDropModule} from '@angular/cdk/drag-drop';



@NgModule({
  declarations: [
                  ViewPageBuilderComponent,
                  EditWidgetComponent,
                  FormAddEditFieldComponent,
                  AddEditPageComponent,
                  ManagePageComponent,
                  AddEditNavigationComponent,
                  ManageNavigationComponent
                ],
  imports: [
    CommonModule,
    MaterialModule,
    SharedModule,
    PipeModule,
    FormsModule,
    ViewPageBuilderRoutingModule,
    DragDropModule
  ],
  entryComponents : [
  ViewPageBuilderComponent,
  EditWidgetComponent,
  FormAddEditFieldComponent,
  AddEditPageComponent,
  ManagePageComponent,
  AddEditNavigationComponent,
  ManageNavigationComponent

  ]
})
export class ViewPageBuilderModule { }
