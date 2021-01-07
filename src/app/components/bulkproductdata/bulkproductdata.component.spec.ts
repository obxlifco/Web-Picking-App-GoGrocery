import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BulkproductdataComponent } from './bulkproductdata.component';

describe('BulkproductdataComponent', () => {
  let component: BulkproductdataComponent;
  let fixture: ComponentFixture<BulkproductdataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BulkproductdataComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BulkproductdataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
