import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { storecategorylistComponent } from './storecategorylist.component';

describe('storecategorylistComponent', () => {
  let component: storecategorylistComponent;
  let fixture: ComponentFixture<storecategorylistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ storecategorylistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(storecategorylistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
