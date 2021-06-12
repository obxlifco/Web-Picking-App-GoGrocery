import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { CookieService, CookieModule } from 'ngx-cookie';
import { MatExpansionModule, MatCardModule, MatStepperModule, MatButtonModule, MatCheckboxModule, MatInputModule, MatTooltipModule, MatTabsModule, MatSelectModule, MatDialogModule, MatRadioModule, MatSnackBarModule, MatProgressSpinnerModule, MatProgressBarModule, MatChipsModule, MatAutocompleteModule, MatMenuModule, MatListModule, MatSlideToggleModule,MatDatepickerModule,MatNativeDateModule} from '@angular/material';
import { MatButtonToggleModule} from '@angular/material/button-toggle';
import { NgxPaginationModule } from 'ngx-pagination';
import { TruncatePipe } from './global/directive/char-count.directive';
import { InputTrimModule } from 'ng2-trim-directive';
import { ConfirmDialog, AlertDialog } from './global/dialog/confirm-dialog.component';
import { TimeFormatPipe } from './global/pipes/convertFrom24To12Format.pipe';
import { EqualValidator, SafeValidator, passwordValidator, MinValidator, MaxValidator } from './global/directive/equal-validator.directive';
import { AccordianDirective } from './global/directive/accordian.directive';
import { PopupImgDirective, ImageUploadUrlDialog, ImageMetaDataDialog, ImageUploadLibDialog } from './global/directive/popup-image.directive';
import { EditorDialog } from './global/directive/editor.directive';
import { CKEditorModule } from 'ng2-ckeditor';
import { DialogsService } from './global/dialog/confirm-dialog.service';
import { SafeHtmlPipe } from './global/pipes/safe-html.pipe';
import { GridComponent, ColumnLayoutComponent } from './global/grid/app.grid-global.component';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { MatIconModule } from '@angular/material/icon';
import { DragDropModule } from '@angular/cdk/drag-drop';

import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';

import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';
import { ReactiveFormsModule} from '@angular/forms';
import { MatFormFieldModule } from '@angular/material';
// import { DatePipe } from '@angular/common';
@NgModule({
  imports: [
    RouterModule,
    CommonModule,
    FormsModule,
    CookieModule.forRoot(),
    MatExpansionModule,
    MatCardModule,
    MatStepperModule,
    MatButtonModule,
    MatCheckboxModule,
    MatInputModule,
    MatTooltipModule,
    MatTabsModule,
    MatSelectModule,
    MatDialogModule,
    MatRadioModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatChipsModule,
    MatAutocompleteModule,
    MatIconModule,
    MatMenuModule,
    MatListModule,
    MatSlideToggleModule,
    MatDatepickerModule,
    MatNativeDateModule,   
    MatButtonToggleModule,
    CKEditorModule,
    NgxPaginationModule,
    NgxSkeletonLoaderModule,
    DragDropModule,
    NgxMatSelectSearchModule,
    ReactiveFormsModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    MatFormFieldModule
  ],
  declarations: [
    EqualValidator,
    SafeValidator,
    passwordValidator,
    MinValidator,
    MaxValidator,
    ConfirmDialog,
    AlertDialog,
    TruncatePipe,
    SafeHtmlPipe,
    TimeFormatPipe,
    AccordianDirective,
    GridComponent,
    ColumnLayoutComponent,
    PopupImgDirective,
    EditorDialog,
    PopupImgDirective,
    ImageUploadUrlDialog,
    ImageMetaDataDialog,
    ImageUploadLibDialog
  ],
  exports:[
    SafeHtmlPipe,
    TruncatePipe,
    NgxPaginationModule,
    NgxSkeletonLoaderModule,
    FormsModule,
    MatInputModule,
    MatCheckboxModule,
    MatRadioModule,
    MatButtonModule,
    MatStepperModule,
    MatCardModule,
    MatExpansionModule,
    MatTooltipModule,
    MatTabsModule,
    MatSelectModule,
    MatTooltipModule,
    MatTabsModule,
    MatDialogModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatChipsModule,
    MatIconModule,
    MatAutocompleteModule,
    MatMenuModule,
    MatListModule,
    MatSlideToggleModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonToggleModule,
    InputTrimModule,
    AccordianDirective,
    GridComponent,
    EditorDialog,
    PopupImgDirective,
    ImageUploadUrlDialog,
    ImageMetaDataDialog,
    ImageUploadLibDialog,
    CKEditorModule,
    DragDropModule,
    NgxMatSelectSearchModule,
    ReactiveFormsModule,
    FormsModule,
    MatFormFieldModule,
    RouterModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
  ],
  providers: [
      DialogsService, CookieService
  ],
  entryComponents: [
    PopupImgDirective,
    ImageUploadUrlDialog,
    ImageMetaDataDialog,
    ImageUploadLibDialog,
    ConfirmDialog,
    EditorDialog,
    AlertDialog,
    ColumnLayoutComponent,
  ]
})
export class BmscommonModule { }