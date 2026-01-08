import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ReceiptService } from '../../services/receipt';

@Component({
  selector: 'amg-receipt-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './receipt-form.html',
  styleUrl: './receipt-form.scss',
})
export class ReceiptFormComponent {
  private fb = inject(FormBuilder);
  private receiptService = inject(ReceiptService);

  // Signal to track loading state
  isSubmitting = signal(false);
  // Add this to your class
  selectedFile: File | null = null;

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      console.log("File ready for 'Snap' logic:", file.name);
    }
  }
  receiptForm = this.fb.group({
    user_id: ['AMG_USER_01'],
    merchant_name: ['', [Validators.required, Validators.minLength(2)]],
    total_amount: [null, [Validators.required, Validators.min(0.01)]],
    purchase_date: [new Date().toISOString().split('T')[0], Validators.required],
  });

  onSubmit() {
    if (this.receiptForm.valid) {
      this.isSubmitting.set(true);

      this.receiptService.submitReceipt(this.receiptForm.value as any).subscribe({
        next: (res) => {
          alert(`Success! You earned ${res.points_earned} points.`);
          this.receiptForm.patchValue({ merchant_name: '', total_amount: null });
          this.isSubmitting.set(false);
        },
        error: (err) => {
          console.error('API Error:', err);
          this.isSubmitting.set(false);
          alert('Submission failed. Is the backend running?');
        },
      });
    }
  }
}
