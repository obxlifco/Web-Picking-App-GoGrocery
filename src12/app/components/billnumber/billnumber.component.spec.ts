import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BillnumberComponent } from './billnumber.component';

describe('BillnumberComponent', () => {
  let component: BillnumberComponent;
  let fixture: ComponentFixture<BillnumberComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BillnumberComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BillnumberComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
