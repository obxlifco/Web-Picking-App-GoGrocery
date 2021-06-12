import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FinetuninglocationComponent } from './finetuninglocation.component';

describe('FinetuninglocationComponent', () => {
  let component: FinetuninglocationComponent;
  let fixture: ComponentFixture<FinetuninglocationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FinetuninglocationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FinetuninglocationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
