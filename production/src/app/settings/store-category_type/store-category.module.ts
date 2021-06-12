import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { BmscommonModule } from '../../bmscommon.module';
import { StoreCategoryRoutingModule } from './store-category-routing.module';

import { StoreCategoryComponent }  from '../../settings/store-category_type/settings.store-category.component';
import { storeCategoryAddEditComponent }  from '../../settings/store-category_type/settings.store-category.addedit.component';
import { GooglePlaceModule } from "ngx-google-places-autocomplete";
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  imports: [
    CommonModule,
    StoreCategoryRoutingModule,
    BmscommonModule,
    GooglePlaceModule,
    NgSelectModule
  ],
  declarations: [
    StoreCategoryComponent,
    storeCategoryAddEditComponent
  ],
  entryComponents: [ 
  	StoreCategoryComponent,
    storeCategoryAddEditComponent
  ]
})
export class StoreCategoryModule { }