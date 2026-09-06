import { ArchivePage } from '@/components/archive-page';
import { nights } from '@/lib/nights';
import { PAGE_SIZE } from '@/lib/archive';
export function generateStaticParams() {
  return Array.from(
    { length: Math.ceil(nights.length / PAGE_SIZE) },
    (_, i) => ({ page: String(i + 1) }),
  );
}
export default async function Page({
  params,
}: {
  params: Promise<{ page: string }>;
}) {
  const { page } = await params;
  return <ArchivePage page={Number(page)} />;
}
