import { TestBed } from '@angular/core/testing';

import { DeliverymanagerService } from './deliverymanager.service';

describe('DeliverymanagerService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DeliverymanagerService = TestBed.get(DeliverymanagerService);
    expect(service).toBeTruthy();
  });
});
