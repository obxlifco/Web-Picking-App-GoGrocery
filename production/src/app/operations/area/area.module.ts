import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AreaRoutingModule } from './area-routing.module';
import { BmscommonModule } from '../../bmscommon.module';
import { AreaAddEditComponent } from './area.addedit.component';
import { AreaComponent, ImportFileAreaComponent } from './area.component';
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
    declarations: [AreaComponent,AreaAddEditComponent,ImportFileAreaComponent,],
  imports: [
    CommonModule,
    AreaRoutingModule,
    BmscommonModule,
    NgSelectModule
  ],
  entryComponents: [ImportFileAreaComponent],
})
export class AreaModule { }
