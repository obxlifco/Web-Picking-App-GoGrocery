import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ListingRoutingModule } from './listing-routing.module';
import { ListingComponent } from "./listing.component";
import { FormsModule } from '@angular/forms';
import {PipeModule} from '../../global/pipes/pipe.module';
import { Ng5SliderModule } from 'ng5-slider';
import { InfiniteScrollModule } from 'ngx-infinite-scroll';
import {
  Location,
  LocationStrategy,
  HashLocationStrategy,
  APP_BASE_HREF
} from '@angular/common';
import {  MatCheckboxModule,MatOptionModule,MatSelectModule,MatRadioModule,
  MatIconModule,MatButtonModule,MatFormFieldModule,MatMenuModule,MatDatepickerModule, MatSlideToggleModule,
  MatRippleModule,
  MatSliderModule,
  MatTabsModule,
  MatNativeDateModule,
  MatChipsModule,
  MatAutocompleteModule,
  MatExpansionModule
} from '@angular/material';

import { NgxPaginationModule } from 'ngx-pagination';

@NgModule({
  declarations: [ListingComponent],
  imports: [

    CommonModule,
    NgxPaginationModule,
    ListingRoutingModule,
    MatCheckboxModule,
    MatOptionModule,
    MatSelectModule,
    MatRadioModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatMenuModule,
    MatDatepickerModule,
    FormsModule,
    MatRippleModule,
    MatSliderModule,
    MatTabsModule,
    MatNativeDateModule,
    MatChipsModule,
    MatAutocompleteModule,
    MatExpansionModule,
    PipeModule,
    Ng5SliderModule,
    InfiniteScrollModule
  ],
  providers: [Location, { provide: LocationStrategy, useClass: HashLocationStrategy }],
})
export class ListingModule { }
