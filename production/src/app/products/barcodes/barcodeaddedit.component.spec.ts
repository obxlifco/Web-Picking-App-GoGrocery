import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BarcodeaddeditComponent } from './barcodeaddedit.component';

describe('BarcodeaddeditComponent', () => {
  let component: BarcodeaddeditComponent;
  let fixture: ComponentFixture<BarcodeaddeditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BarcodeaddeditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BarcodeaddeditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
