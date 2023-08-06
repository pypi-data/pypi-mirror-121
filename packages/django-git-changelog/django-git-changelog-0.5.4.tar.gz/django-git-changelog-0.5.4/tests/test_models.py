from django.test.testcases import TestCase
from pathlib import Path
from changelog.models import Repository, Branch, Commit, Tag
from django.conf import settings
from changelog import __version__, get_version
from git.cmd import Git


class TestRepositoryMixin(TestCase):
    def setUp(self):
        self.repository = Repository(
            path=Path(__file__).parent.parent,
            name='test',
        )


class TestSavedRepositoryMixin(TestRepositoryMixin):
    def setUp(self):
        super().setUp()
        self.repository.save()


class TestRepositoryModel(TestRepositoryMixin):
    def test_save_and_refresh(self):
        ''' before saving '''
        repository = self.repository
        self.assertIsNone(repository.id)
        self.assertFalse(Branch.objects.all())
        self.assertFalse(Commit.objects.all())
        self.repository.save()
        
        ''' after saving '''
        self.assertIsInstance(repository.id, int)
        self.assertTrue(Branch.objects.all())
        self.assertTrue(Commit.objects.all())

        ''' Reset and refresh '''
        Branch.objects.all().delete()
        Commit.objects.all().delete()
        repository.refresh()
        self.assertTrue(Branch.objects.all())
        self.assertTrue(Commit.objects.all())

    def test_clean(self):
        ''' Test without path to autofill basedir '''
        repository = Repository(name='foo')
        self.assertEqual(repository.path, '')
        repository.clean()
        self.assertEqual(repository.path, settings.BASE_DIR)

        ''' And now create relative path '''
        repository = Repository(name='foo', path='relative/')
        repository.clean()
        self.assertEqual(repository.path, str(settings.BASE_DIR) + '/relative/')

    def test_git(self):
        self.assertIsInstance(self.repository.git.show(), str)

    def test_get_version(self):
        self.assertEqual(self.repository.get_version(), __version__)
        self.assertEqual(self.repository.get_version(), get_version())

    def test_str(self):
        self.assertEqual(str(self.repository), self.repository.name)


class TestBranchModel(TestSavedRepositoryMixin):
    def test_branch(self):
        branch = Branch.objects.first()
        self.assertEqual(
            str(branch), f'{branch.repository.name}: {branch.name}'
        )


class TestCommitModel(TestSavedRepositoryMixin):
    
    def test_properties(self):
        commit = Commit.objects.first()
        self.assertEqual(commit.message, commit.commit.message)
        self.assertIsInstance(commit.git, Git)

        ''' Commit.commit '''
        git_commit = commit.commit
        self.assertEqual(commit.id, git_commit.hexsha)

        ''' Commit.body '''
        commit.message = 'testhead\ntestbody'
        self.assertEqual(commit.head, 'testhead')
        self.assertEqual(commit.body, 'testbody')

        ''' Commit.stat '''
        self.assertIsInstance(commit.stat, str)

        ''' Commit.details '''
        self.assertIsInstance(commit.details, str)

        ''' Commit.files '''
        self.assertIsInstance(commit.files, str)

        ''' Commit.all_files '''
        self.assertIsInstance(commit.all_files, str)
        
        ''' Commit.__str__ '''
        self.assertEqual(str(commit), commit.head)


class TestTagModel(TestSavedRepositoryMixin):
    def test_str(self):
        tag = Tag.objects.first()
        if not tag:
            tag = Tag(name='testname')
        self.assertEqual(str(tag), tag.name)
