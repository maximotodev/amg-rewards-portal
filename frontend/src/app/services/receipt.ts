import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

export interface Receipt {
  id?: number;
  user_id: string;
  merchant_name: string;
  total_amount: number;
  purchase_date: string;
  status?: string;
  points_earned?: number;
}

@Injectable({
  providedIn: 'root',
})
export class ReceiptService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/v1/receipts';

  receipts = signal<Receipt[]>([]);

  fetchReceipts(): void {
    this.http.get<Receipt[]>(this.apiUrl).subscribe((data) => {
      this.receipts.set(data);
    });
  }

  /**
   * Atomic Submission: Packages metadata and binary image into one FormData request.
   */
  submitReceipt(receipt: Receipt, imageFile: File): Observable<Receipt> {
    const formData = new FormData();
    formData.append('user_id', receipt.user_id);
    formData.append('merchant_name', receipt.merchant_name);
    formData.append('total_amount', receipt.total_amount.toString());
    formData.append('purchase_date', receipt.purchase_date);
    formData.append('image', imageFile);

    return this.http.post<Receipt>(this.apiUrl, formData).pipe(tap(() => this.fetchReceipts()));
  }
}
