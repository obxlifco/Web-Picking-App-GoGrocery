import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxratesComponent } from './taxrates.component';

describe('TaxratesComponent', () => {
  let component: TaxratesComponent;
  let fixture: ComponentFixture<TaxratesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxratesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxratesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
