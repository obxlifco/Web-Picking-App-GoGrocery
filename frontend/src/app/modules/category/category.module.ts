import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import {  } from '@angular/material/checkbox';
import {  MatCheckboxModule,MatOptionModule,MatSelectModule,MatRadioModule,MatIconModule,MatButtonModule,MatFormFieldModule,MatMenuModule,MatDatepickerModule} from '@angular/material';

import { CategoryRoutingModule } from './category.routing.module'; 

import { CategoryComponent }  from './category.component';




// import { MatSlideToggleModule} from '@angular/material/slide-toggle';

// import { MatInputModule, MatRippleModule, MatSliderModule, MatTabsModule, 
//   MatNativeDateModule, MatChipsModule, MatAutocompleteModule, MatExpansionModule} from '@angular/material';
@NgModule({
  imports: [
    CommonModule,
    CategoryRoutingModule,
    MatCheckboxModule,
    MatOptionModule,
    MatSelectModule,
    MatRadioModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatMenuModule,
    MatDatepickerModule
      ],
  declarations: [
  	CategoryComponent
  ],
  entryComponents: [
  	CategoryComponent
  ]
})
export class CategoryModule { }
