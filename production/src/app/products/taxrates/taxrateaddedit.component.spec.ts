import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxrateaddeditComponent } from './taxrateaddedit.component';

describe('TaxrateaddeditComponent', () => {
  let component: TaxrateaddeditComponent;
  let fixture: ComponentFixture<TaxrateaddeditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxrateaddeditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxrateaddeditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
